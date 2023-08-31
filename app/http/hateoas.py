from ..middleware.middleware import request_object
from typing import TypeVar, Generic


class HrefProvider:
    @staticmethod
    def get_url_with_params(params: dict[str, str]={}):
        request = request_object.get()
        return request.url.include_query_params(**params)

    @staticmethod
    def get_url(path: str):
        request = request_object.get()
        base_url = str(request.base_url)
        return base_url + path


T = TypeVar("T")


class HateoasManager(Generic[T]):
    def __init__(
        self,
        dataset: list,
        path: str,
        key: str | None = None,
        ref: str | int | None = None,
        href_name: str = "href",
    ):
        self.path = path
        self.dataset = dataset
        self.key = key
        self.ref = ref
        self.href_name = href_name

    def __set_url(self, item: T):
        id = self.ref or (getattr(item, self.key) if self.key else "")
        if hasattr(item, self.href_name):
            setattr(item, self.href_name, HrefProvider.get_url(f"{self.path}/{id}"))

    def set_urls(self):
        for item in self.dataset:
            self.__set_url(item)
