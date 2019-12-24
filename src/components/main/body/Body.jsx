import React, { useState } from 'react';
import NCFilter from '../header/NCFilter';
import DataPicker from '../header/DataPicker';
import PinMap from '../../PinMap/PinMap';
import Legend from '../header/Legend';

const Body = ({
  data,
  link,
  buildUrl,
  updateState,
  startMonth,
  endMonth,
}) => {
  const [isGenerating, setIsGenerating] = useState(false);

  const handleOnGenerateClick = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setIsGenerating(false);
    }, 1000);
    buildUrl();
  }

  
  return (
    <>
      <div className="level">
        <div className="level-item">
          Welcome to the beta version of our Los Angeles neighborhood 311 report generator.
          <br />
          This 1st report will give you a list of the addresses with the highest incidence of the 311 issue that you select.
          <br /> 
          Hack for LA is a group of volunteers helping our community one software project at a time. 
          <br />
          Please feel free to contact us with any feedback you have in order to improve this tool. 
          <br />
          Thank you!
        </div>
      </div>
      <div className="container">
        <div className="field">
          <label className="label">
            Neighborhood Council
          </label>

          <div className="control">
            <div className="select">
              <NCFilter />
            </div>
          </div>
        </div>

        <div className="field">
          <div className="control">
            <DataPicker
              onDropdownSelect={updateState}
              startMonth={startMonth}
              endMonth={endMonth}
            />
          </div>
        </div>
      </div>
      <div className="level">
        <div className="level-item">
          <button 
            className={`button is-link ${isGenerating ? 'is-loading' : null}`}
            type="button"
            onClick={handleOnGenerateClick}
          >
              Generate Link
          </button>
        </div>
      </div>
      <div className="level">
        <div className="level-item">
          {link && !isGenerating && (
            <a href={link}>
              Click Here to Download Report
            </a>
          )}
        </div>
      </div>
      {/* <div className="columns">
        <div className="column is-2">
          <Legend />
        </div>
        <div className="column">
          <PinMap
            showMarkers={showMarkers}
            data={data}
            onDropdownSelect={updateState}
            toggleShowMarker={toggleShowMarkers}
          />
        </div>
      </div> */}
    </>
  );
};

export default Body;
