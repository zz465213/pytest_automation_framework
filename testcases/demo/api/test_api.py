import allure
import os
import pytest
from configs import global_adapter
from configs.common_paths import CONFIGS_FILE, PAYLOADS_DIR
from utils.api_factory import APIFactory
from utils.file_tool import read_json, read_yaml


@allure.epic("JSONPlaceholder")
@pytest.mark.jph
@pytest.mark.api
class TestJPH:
    jph_payload = read_json(os.path.join(PAYLOADS_DIR, "jph.json"))
    jph_url = read_yaml(CONFIGS_FILE)[global_adapter.ENV]["jph"]["url"]

    @allure.feature("Get 測試")
    def test_get_post_id1(self):
        # Given
        jph_api = APIFactory(self.jph_url)
        id_no = 1
        # When
        get_id = jph_api.get_json(f"/comments?postId={id_no}")
        # Then
        jph_api.assert_equal(get_id[0]["postId"], 1)

    @allure.feature("Post 測試")
    def test_posts(self):
        # Given
        jph_api = APIFactory(self.jph_url)
        headers = self.jph_payload["posts_headers"]
        headers["User-Agent"] = "Safari/537.36"
        headers["Connection"] = "keep-alive"
        body = self.jph_payload["posts_body"]
        body["title"] = "更改後的文章標題"
        # When
        posts_json = jph_api.post("/posts", json=body, headers=headers)
        # Then
        jph_api.assert_equal(posts_json.json()["title"], body["title"])
        jph_api.assert_equal(posts_json.json()["body"], body["body"])
        jph_api.assert_equal(posts_json.json()["userId"], body["userId"])
