import os
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS
from sanic_gzip import Compress
from configparser import ConfigParser
from threading import Timer
from datetime import datetime
from multiprocessing import cpu_count

from services.time_to_close import time_to_close
from services.frequency import frequency
from services.pinService import PinService
from services.requestCountsService import RequestCountsService
from services.requestDetailService import RequestDetailService
from services.ingress_service import ingress_service
from services.sqlIngest import DataHandler

app = Sanic(__name__)
CORS(app)
compress = Compress()


def environment_overrides():
    if os.environ.get('DB_CONNECTION_STRING', None):
        app.config['Settings']['Database']['DB_CONNECTION_STRING'] =\
            os.environ.get('DB_CONNECTION_STRING')
    if os.environ.get('PORT', None):
        app.config['Settings']['Server']['PORT'] =\
            os.environ.get('PORT')
    if os.environ.get('TOKEN', None):
        app.config['Settings']['Socrata']['TOKEN'] =\
            os.environ.get('TOKEN')

#settings_check() verifies if 'settings.cfg' contains all the keys in 'settings.example.cfg'.
#args: takes a ConfigParser object
#returns: boolean
def settings_check(settings_config):
    #read example config's file
    example_config = ConfigParser()
    example_config.read(os.path.join(os.getcwd(), 'settings.example.cfg'))
    #compare example's and setting's keys
    missing_keys_msg = []
    for example_section in example_config.sections():
        example_keys = set([i[0] for i in example_config.items(example_section)])
        #if section doesn't exist in 'settings.cfg', create an empty set.
        try:
            settings_keys = set([i[0] for i in settings_config.items(example_section)])
        except:
            settings_keys = set()
        diff_keys = example_keys - settings_keys
        #if elements exist in diff_keys, add the missing keys to output as "[section] key"
        if(diff_keys):
            #Note, extra keys in settings will logically end up here. however, they wont add to the output.
            missing_keys = diff_keys & example_keys
            for m_key in missing_keys:
                missing_keys_msg.append("[" + str(example_section).title() + "] " + str(m_key).upper())
    #if elements exist in missing keys output, print output and return false.
    if(missing_keys_msg):
        print("'Settings.cfg is missing keys from 'settings.example.cfg'. Please check for these keys below:")
        for keys_msg in missing_keys_msg:
            print(keys_msg)
        return False
    return True
        
def configure_app():
    # Settings initialization
    config = ConfigParser()
    settings_file = os.path.join(os.getcwd(), 'settings.cfg')
    config.read(settings_file)
    #if 'settings.cfg' has the expected keys, set app's config with those values.
    if(settings_check(config)):
        app.config['Settings'] = config
        environment_overrides()
        app.config["STATIC_DIR"] = os.path.join(os.getcwd(), "static")
        os.makedirs(os.path.join(app.config["STATIC_DIR"], "temp"), exist_ok=True)
        return True
    return False


@app.route('/')
@compress.compress()
async def index(request):
    return json('You hit the index')


@app.route('/timetoclose', methods=["POST"])
@compress.compress()
async def timetoclose(request):
    ttc_worker = time_to_close(app.config['Settings'])

    postArgs = request.json
    start = postArgs.get('startDate', None)
    end = postArgs.get('endDate', None)
    ncs = postArgs.get('ncList', [])
    requests = postArgs.get('requestTypes', [])

    data = ttc_worker.ttc(startDate=start,
                          endDate=end,
                          ncList=ncs,
                          requestTypes=requests)
    return json(data)


@app.route('/requestfrequency')
@compress.compress()
async def requestfrequency(request):
    freq_worker = frequency(app.config['Settings'])

    data = freq_worker.freq_view_data(service=True,
                                      councils=[],
                                      aggregate=True)

    return json(data)


@app.route('/sample-data')
@compress.compress()
async def sample_route(request):
    sample_dataset = {'cool_key': ['value1', 'value2'],
                      app.config['REDACTED']: app.config['REDACTED']}
    return json(sample_dataset)


@app.route('/ingest', methods=["POST"])
@compress.compress()
async def ingest(request):
    """Accept POST requests with a list of years to import.
        Query parameter name is 'years', and parameter value is
        a comma-separated list of years to import.
        Ex. '/ingest?years=2015,2016,2017'
    """
    current_year = datetime.now().year
    querySize = request.args.get("querySize", None)
    limit = request.args.get("limit", None)
    ALLOWED_YEARS = [year for year in range(2015, current_year+1)]
    if not request.args.get("years"):
        return json({"error": "'years' parameter is required."})
    years = set([int(year) for year in request.args.get("years").split(",")])
    if not all(year in ALLOWED_YEARS for year in years):
        return json({"error":
                    f"'years' param values must be one of {ALLOWED_YEARS}"})
    loader = DataHandler(app.config['Settings'])
    loader.populateFullDatabase(yearRange=years,
                                querySize=querySize,
                                limit=limit)
    return_data = {'response': 'ingest ok'}
    return json(return_data)


@app.route('/update')
@compress.compress()
async def update(request):
    ingress_worker = ingress_service()
    return_data = ingress_worker.update()
    return json(return_data)


@app.route('/delete')
@compress.compress()
async def delete(request):
    ingress_worker = ingress_service()
    return_data = ingress_worker.delete()
    return json(return_data)


@app.route('/pins', methods=["POST"])
@compress.compress()
async def pinMap(request):
    pin_worker = PinService(app.config['Settings'])
    postArgs = request.json
    start = postArgs.get('startDate', '2015-01-01')
    end = postArgs.get('endDate', '2015-12-31 01:01:01')
    ncs = postArgs.get('ncList', ['SHERMAN OAKS NC'])
    requests = postArgs.get('requestTypes', ['Bulky Items'])

    return_data = await pin_worker.get_base_pins(startDate=start,
                                                 endDate=end,
                                                 ncList=ncs,
                                                 requestTypes=requests)
    return json(return_data)


@app.route('/requestcounts', methods=["POST"])
@compress.compress()
async def requestCounts(request):
    counts_worker = RequestCountsService(app.config['Settings'])
    postArgs = request.json
    start = postArgs.get('startDate', None)
    end = postArgs.get('endDate', None)
    ncs = postArgs.get('ncList', [])
    requests = postArgs.get('requestTypes', [])
    countFields = postArgs.get('countFields', [])

    return_data = await counts_worker.get_req_counts(startDate=start,
                                                     endDate=end,
                                                     ncList=ncs,
                                                     requestTypes=requests,
                                                     countFields=countFields)
    return json(return_data)


@app.route('/servicerequest/<srnumber>', methods=["GET"])
async def requestDetails(request, srnumber):
    detail_worker = RequestDetailService(app.config['Settings'])

    return_data = await detail_worker.get_request_detail(srnumber)
    return json(return_data)


@app.route('/test_multiple_workers')
@compress.compress()
async def test_multiple_workers(request):
    Timer(10.0, print, ["Timer Test."]).start()
    return json("Done")


if __name__ == '__main__':
    if(configure_app()):
        worker_count = max(cpu_count()//2, 1)
        app.run(host=app.config['Settings']['Server']['HOST'],
                port=int(app.config['Settings']['Server']['PORT']),
                workers=worker_count,
                debug=app.config['Settings']['Server']['DEBUG'])
