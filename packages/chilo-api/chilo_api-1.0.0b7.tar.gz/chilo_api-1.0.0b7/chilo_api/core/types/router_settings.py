from enum import Enum
from typing import TypedDict, Callable, Optional


class Cache(Enum):
    ALL = 'all'
    STATIC = 'static-only'
    DYNAMIC = 'dynamic-only'


class RouterSettings(TypedDict):
    handlers: str
    base_path: str
    host: str
    port: int
    reload: bool
    verbose: bool
    before_all: Optional[Callable]
    after_all: Optional[Callable]
    when_auth_required: Optional[Callable]
    on_error: Optional[Callable]
    on_timeout: Optional[Callable]
    cors: bool
    cache_size: Optional[int]
    cache_mode: Cache
    timeout: Optional[int]
    output_error: bool
    openapi: Optional[str]
    openapi_validate_request: bool
    openapi_validate_response: bool
