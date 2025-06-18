import requests
import logging


class APIFactory:
    def __init__(self, url):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.base_url = url
        self.logger.info(f"⚪ Base URL: {self.base_url}")

    def _send_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"⚪ 使用 {method.upper()} 方法到網址: {url}")
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # 對於狀態 400 ~ 599 拋出 HTTPError
            self.logger.info(f"🟢 成功接收到 {url} 的回應 - Statu={response.status_code}")
            return response
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"🔴 {url} 錯誤 Statu={e.response.status_code} - 產生 HTTP 錯誤: {e.response.text}")
            raise
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"🔴 {url} 產生連線錯誤: {e}")
            raise
        except requests.exceptions.Timeout as e:
            self.logger.error(f"🔴 {url} 產生超時錯誤: {e}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"🔴 {url} 產生非預期錯誤: {e}")
            raise

    def get(self, endpoint, params=None, **kwargs):
        return self._send_request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._send_request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._send_request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._send_request("DELETE", endpoint, **kwargs)

    def get_json(self, endpoint, params=None, **kwargs):
        return self.get(endpoint, params=params, **kwargs).json()

    def get_text(self, endpoint, params=None, **kwargs):
        return self.get(endpoint, params=params, **kwargs).text

    def get_content(self, endpoint, params=None, **kwargs):
        return self.get(endpoint, params=params, **kwargs).content

    def get_raw(self, endpoint, params=None, **kwargs):
        return self.get(endpoint, params=params, **kwargs).raw

    def assert_equal(self, expect_result, actual_result):
        """
        斷言預期結果與實際結果是否相等。
        """
        try:
            assert expect_result == actual_result
            self.logger.info(f"🟢 PASSED - 預期結果: {expect_result}, 實際結果: {actual_result}")
        except AssertionError as e:
            error_msg = f"🔴 FAILED - 預期结果: {expect_result}, 實際結果: {actual_result}, 錯誤訊息: {e}"
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"🔴 FAILED - 斷言過程發生非預期錯誤:{e}, 預期结果: {expect_result}, 實際結果: {actual_result}"
            raise Exception(error_msg)

    def assert_include(self, expect_result, actual_result):
        """
        斷言預期結果是否包含在實際結果中。
        """
        try:
            assert expect_result in actual_result
            self.logger.info(f"🟢 PASSED - 預期結果: {expect_result}, 實際結果: {actual_result}")
        except AssertionError as e:
            error_msg = f"🔴 FAILED - 預期结果: {expect_result}, 實際結果: {actual_result}, 錯誤訊息: {e}"
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"🔴 FAILED - 斷言過程發生非預期錯誤:{e}, 預期结果: {expect_result}, 實際結果: {actual_result}"
            raise Exception(error_msg)