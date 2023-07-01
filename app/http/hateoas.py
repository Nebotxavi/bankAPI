from ..middleware.middleware import request_object
from typing import List


class HrefProvider:
    @staticmethod
    def get_url_with_params(params={}):
        request = request_object.get()
        return request.url.include_query_params(**params)

    @staticmethod
    def get_url(path: str):
        request = request_object.get()
        base_url = str(request.base_url)

        return base_url + path


class HateoasManager:
    def __init__(
            self,
            dataset: List,
            path: str,
            key: str | None = None,
            ref: str | int | None = None):
        self.path = path
        self.dataset = dataset
        self.key = key
        self.ref = ref

    def __set_url(self, item):
        id = self.ref or getattr(item, self.key) if self.key else ""
        item.href = str(HrefProvider.get_url(f'{self.path}/{id}'))

    def set_urls(self):
        for item in self.dataset:
            self.__set_url(item)
