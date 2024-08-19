import asyncio
import typing as t

_not_set: t.Any = object()


class HttpClientProtocol(t.Protocol):
    def get(self, url: str, **kwargs: t.Any) -> t.Any: ...

    def post(self, url: str, **kwargs: t.Any) -> t.Any: ...

    def patch(self, url: str, **kwargs: t.Any) -> t.Any: ...


class RequestProtocol(dict[str, t.Any]):
    pass


class ResponseProtocol(t.Protocol):
    status_code: int

    def json(self) -> dict[str, t.Any]: ...


class BaseClientError(BaseException):
    codes_mapping: dict[int, t.Callable[[], type["BaseClientError"]]] = {}

    @classmethod
    async def from_response(cls, url: str, request: RequestProtocol, response: ResponseProtocol):
        return cls.codes_mapping.get(response.status_code, lambda: cls)()(url, request, response)

    def __str__(self):
        return f"Request {self.url=} {self.request=}, invalid response: {self.response=}, {self.response.json()}"

    def __init__(self, url: str, request: RequestProtocol, response: ResponseProtocol):
        self.url = url
        self.request = request
        self.response = response
        self.status = response.status_code


class BaseAPIClient:
    base_url: str
    error_class: type[BaseClientError] | None = BaseClientError

    async def _make_request(
        self,
        client_method: str,
        url: str,
        *,
        data: dict[str, t.Any] | None = _not_set,
        timeout: int | None = _not_set,
    ) -> t.Any:
        url = self.base_url + url
        kwargs: dict[str, t.Any] = {}
        if data is not _not_set:
            kwargs["json"] = data
        if client_method.lower() in ("put", "post"):
            kwargs.setdefault("headers", {})
            kwargs["headers"]["Content-Type"] = "application/json"
        kwargs["timeout"] = timeout if timeout is not _not_set else None
        response = getattr(self.client, client_method)(url, **kwargs)
        if asyncio.iscoroutine(response):
            response = await response
        return await self._process_response(response, url, kwargs)

    async def _process_response(self, response: ResponseProtocol, url: str, kwargs: t.Any) -> t.Any:
        if not self._is_successful_response(response):
            return await self._process_unsuccessful_response(url, kwargs, response)
        return await self._get_response_content(response)

    def _is_successful_response(self, response: ResponseProtocol) -> bool:
        return response.status_code < 400

    async def _process_unsuccessful_response(
        self, url: str, kwargs: RequestProtocol, response: ResponseProtocol
    ) -> None:
        if not self.error_class:
            raise RuntimeError("No error class")
        exception = self.error_class.from_response(url, kwargs, response)
        if asyncio.iscoroutine(exception):
            _exception = await exception
        else:
            _exception = exception
        raise _exception

    async def _get_response_content(self, response: ResponseProtocol) -> t.Any:
        response_json = response.json()
        if asyncio.iscoroutine(response_json):
            return await response_json
        return response_json

    def __init__(self, client: HttpClientProtocol) -> None:
        self.client = client
