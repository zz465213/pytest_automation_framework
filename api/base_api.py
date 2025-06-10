import requests
import logging


class BaseAPI:
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
