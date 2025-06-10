import allure
import os
import pytest
from api.jph_api import JphAPI
from configs import global_adapter
from configs.common_paths import CONFIGS_FILE, PAYLOADS_DIR
from utils.file_tool import read_json, read_yaml


@allure.epic("JSONPlaceholder")
@pytest.mark.jph
class TestJPH:
    jph_payload = read_json(os.path.join(PAYLOADS_DIR, "jph.json"))
    jph_url = read_yaml(CONFIGS_FILE)[global_adapter.ENV]["jph"]["url"]

    @allure.feature("Get 測試")
    def test_get_post_id1(self):
        # Given
        jph_api = JphAPI(self.jph_url, 2)
        # When
        get_id101 = jph_api.get_id().json()
        # Then
        assert get_id101[0]["postId"] == 2

    @allure.feature("Post 測試")
    def test_posts(self):
        # Given
        global_adapter.URL = self.jph_url
        jph_api = JphAPI(self.jph_url, 10)

        headers = self.jph_payload["posts_headers"]
        headers["User-Agent"] = "Safari/537.36"  # 新增資訊
        headers["Connection"] = "keep-alive"

        body = self.jph_payload["posts_body"]
        body["title"] = "更改後的文章標題"  # 更改資訊
        # When
        posts_json = jph_api.posts(json=body, headers=headers)
        # Then
        assert posts_json.json()["title"] == body["title"]
        assert posts_json.json()["body"] == body["body"]
        assert posts_json.json()["userId"] == body["userId"]
