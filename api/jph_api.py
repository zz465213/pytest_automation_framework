import logging
from api.base_api import BaseAPI


class JphAPI(BaseAPI):

    def __init__(self, url, id_no=1):
        super().__init__(url)
        self.logger = logging.getLogger(__name__)
        self.get_id_endpoint = f"/comments?postId={id_no}"
        self.posts_endpoint = "/posts"

    def get_id(self):
        """使用get獲取對應id的資料"""
        return self.get(self.get_id_endpoint)

    def posts(self, **kwargs):
        return self.post(self.posts_endpoint, **kwargs)
