from configs import global_adapter
from configs.common_paths import CONFIGS_FILE
import pytest
from utils.file_tool import read_yaml


@pytest.fixture(scope="session")
def get_url():
    """根據環境讀取配置，取得該資料夾下測案URL"""
    _url = read_yaml(CONFIGS_FILE)["yahoo"][global_adapter.ENV]["url"]
    if _url:
        global_adapter.URL = _url
    return global_adapter.URL
