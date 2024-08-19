from enum import Enum
from typing import TypedDict, Callable, Optional


class Cache(Enum):
    ALL = 'all'
    STATIC = 'static-only'
    DYNAMIC = 'dynamic-only'


class RouterSettings(TypedDict):
    handlers: str
    base_path: str
    host: str = '127.0.0.1'
    port: int = 3000
    reload: bool = False
    verbose: bool = False
    before_all: Optional[Callable]
    after_all: Optional[Callable]
    when_auth_required: Optional[Callable]
    on_error: Optional[Callable]
    on_timeout: Optional[Callable]
    cors: bool = True
    cache_size: Optional[int]
    cache_mode: Cache = 'all'
    timeout: Optional[int]
    output_error: bool = False
    openapi: Optional[str]
    openapi_validate_request: bool = False
    openapi_validate_response: bool = False
