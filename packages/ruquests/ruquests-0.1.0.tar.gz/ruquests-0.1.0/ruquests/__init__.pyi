from typing import Any

class ResponseLines:
    def next(self) -> str: ...

class Response:
    @property
    def status_code(self) -> int: ...
    @property
    def headers(self) -> dict[str, str]: ...
    def raise_for_status(self) -> None: ...
    def json(self) -> Any: ...
    def text(self) -> str: ...
    def bytes(self) -> bytes: ...
    def iter_lines(self) -> ResponseLines: ...

class Request:
    def send(self) -> Response: ...

def head(
    url: str,
    headers: dict[str, str] | None = None,
    timeout: int | None = None,
) -> Request: ...
def get(
    url: str,
    query_params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    follow_redirects: bool | None = None,
    timeout: int | None = None,
) -> Request: ...
def post(
    url: str,
    query_params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    json: Any | None = None,
    data: dict[str, str] | None = None,
    form: Any | None = None,
    follow_redirects: bool | None = None,
    timeout: int | None = None,
) -> Request: ...
def put(
    url: str,
    query_params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    json: Any | None = None,
    data: dict[str, str] | None = None,
    form: Any | None = None,
    follow_redirects: bool | None = None,
    timeout: int | None = None,
) -> Request: ...
def patch(
    url: str,
    query_params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    json: Any | None = None,
    data: dict[str, str] | None = None,
    form: Any | None = None,
    follow_redirects: bool | None = None,
    timeout: int | None = None,
) -> Request: ...
def delete(
    url: str,
    query_params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    json: Any | None = None,
    data: dict[str, str] | None = None,
    form: Any | None = None,
    follow_redirects: bool | None = None,
    timeout: int | None = None,
) -> Request: ...
