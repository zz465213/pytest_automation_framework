import os
import pytest
from configs import global_adapter
from configs.common_paths import CONFIGS_FILE, PAYLOADS_DIR
from utils.file_tool import read_yaml, read_json


@pytest.fixture(scope="session")
def get_url():
    url = read_yaml(CONFIGS_FILE)[global_adapter.ENV]["heroku_app"]["url"]
    if url:
        global_adapter.URL = url
    return global_adapter.URL


@pytest.fixture(scope="function")
def get_username():
    username = read_yaml(CONFIGS_FILE)[global_adapter.ENV]["heroku_app"]["username"]
    return username


@pytest.fixture(scope="function")
def get_password():
    password = read_yaml(CONFIGS_FILE)[global_adapter.ENV]["heroku_app"]["password"]
    password = os.environ.get(password)  # 取環境變數
    return password


@pytest.fixture(scope="function")
def get_json():
    return read_json(f"{PAYLOADS_DIR}/herokuapp.json")

