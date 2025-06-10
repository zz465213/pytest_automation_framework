import pytest
from configs import global_adapter
from configs.common_paths import CONFIGS_FILE
from utils.file_tool import read_yaml


@pytest.fixture(scope="session")
def get_url():
    _url = read_yaml(CONFIGS_FILE)[global_adapter.ENV]["yahoo"]["url"]
    if _url:
        global_adapter.URL = _url
    return global_adapter.URL
