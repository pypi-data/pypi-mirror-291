from typing import TypedDict, Callable, Optional, List, Any


class RequirementSettings(TypedDict):
    required_headers: Optional[List[str]]
    available_headers: Optional[List[str]]
    required_query: Optional[List[str]]
    available_query: Optional[List[str]]
    required_body: Optional[Any]
    required_path: Optional[str]
    required_response: Optional[Any]
    auth_required: Optional[bool]
    before: Optional[Callable]
    after: Optional[Callable]
    request_class: Optional[Any]
    timeout: Optional[int]
    custom: Optional[Any]
    summary: Optional[str]
    deprecated: Optional[bool]
