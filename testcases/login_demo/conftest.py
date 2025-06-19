import pytest
from configs import global_adapter
from configs.common_paths import CONFIGS_FILE, PAYLOADS_DIR
from utils.file_tool import read_yaml, read_json


@pytest.fixture(scope="session")
def get_url():
    _url = read_yaml(CONFIGS_FILE)[global_adapter.ENV]["heroku_app"]["url"]
    if _url:
        global_adapter.URL = _url
    return global_adapter.URL


@pytest.fixture(scope="function")
def get_username():
    _url = read_yaml(CONFIGS_FILE)[global_adapter.ENV]["heroku_app"]["username"]
    if _url:
        global_adapter.URL = _url
    return global_adapter.URL


@pytest.fixture(scope="function")
def get_password():
    _url = read_yaml(CONFIGS_FILE)[global_adapter.ENV]["heroku_app"]["password"]
    if _url:
        global_adapter.URL = _url
    return global_adapter.URL


@pytest.fixture(scope="function")
def get_json():
    return read_json(f"{PAYLOADS_DIR}/herokuapp.json")

