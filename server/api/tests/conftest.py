import time
import os
import subprocess
from pathlib import Path
import asyncio

import pytest
from starlette.testclient import TestClient

import sys
from os.path import join, dirname


# manually adding python paths due to VS code bug
sys.path.append(join(dirname(__file__), '../code'))

# set env setting to ensure _test DB is used by pytests
os.environ["TESTING"] = "True"

from lacity_data_api.asgi import app  # noqa
from lacity_data_api.models import db as test_database  # noqa


@pytest.fixture(scope="session")
def db():
    yield test_database


# (!) this allows async io and starlette tests to coexist w/shared event loop
# guidance from https://github.com/pytest-dev/pytest-asyncio/issues/169
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client(event_loop):

    cwd = Path(__file__).parent.parent

    # init the database
    try:
        subprocess.check_call(["alembic", "upgrade", "head"], cwd=cwd)
    except subprocess.CalledProcessError as identifier:
        print(identifier)

    # create the client for use by tests
    with TestClient(app) as client:
        yield client

    # giving sentry a moment to send before quitting
    time.sleep(1)

    # reset the database
    # if os.environ["TESTING"] is True:
    #     try:
    #         subprocess.check_call(["alembic", "downgrade", "base"], cwd=cwd)
    #     except subprocess.CalledProcessError as identifier:
    #         print(identifier)
