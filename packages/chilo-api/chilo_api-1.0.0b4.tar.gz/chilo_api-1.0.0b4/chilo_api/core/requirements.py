import inspect
import signal
from typing_extensions import Unpack

from chilo_api.core.exception import ApiTimeOutException
from chilo_api.core.request import Request
from chilo_api.core.response import Response
from chilo_api.core.types.requirement_settings import RequirementSettings


def requirements(**kwargs: Unpack[RequirementSettings]):
    '''
    All available parameters you can use with requirements, allows for custom params to be sent either directly as additional kwargs or if 
    using type checkers, can be passed in through the `custom=` param

    Parameters
    ----------
    required_headers: list[str] (optional)
        list of required headers for the request
    available_headers: list[str] (optional)
        list of available headers for the request; is strict and will raise error on ANY additional headers
    required_query: list[str] (optional)
        list of required query string params for the request
    available_query: list[str] (optional)
        list of available query string params for the request
    required_body: str, dict, pydantic model (optional)
        required body for the request to pass validation; can be a string reference to a schema defined in the openapi, a dict in the jsonschema structure or a pydantic model
    required_path: str (optional)
        the path required hit this endpoint; required for dynamic endpoints
    required_response: str (optional)
        the body requirements for the response
    auth_required: bool (optional)
        whether this endpoint requires authentiction; will automatically trigger function defined in when_auth_required (if available)
    before: callable (optional)
        function to run before the method is called
    after: callable (optional)
        function to run after the method is called
    request_class: any (optional)
        class to send instead of a standard request class; this class will get a kwarg, request=request, which is the standard request class
    timeout: int (optional)
        how long the endpoint has to run, will override any value provided in the Chilo class definition
    custom: any (optional)
        add additional custom params here, will be passed to before_all, before, after, after_all, when_auth_required
    summary: str (optional)
        will fill out summary key in openapi file when generated
    deprecated: bool (optional)
        will fill out deprecated field in openapi file when generated (default is False)
    '''
    def decorator_func(func):

        def raise_timeout(*_):
            raise ApiTimeOutException()

        def start_timeout(timeout=None):
            if kwargs.get('timeout') is not None or timeout is not None:
                countdown = kwargs['timeout'] if kwargs.get('timeout') is not None else timeout
                signal.signal(signal.SIGALRM, raise_timeout)
                signal.alarm(countdown)

        def end_timeout():
            signal.alarm(0)

        def run_before(request: Request, response: Response):
            if kwargs.get('before') and callable(kwargs['before']):
                kwargs['before'](request, response, kwargs)

        def run_after(request: Request, response: Response):
            if kwargs.get('after') and callable(kwargs['after']):
                kwargs['after'](request, response, kwargs)

        def run_method(request: Request, response: Response):
            run_before(request, response)
            start_timeout(request.timeout)
            if not response.has_errors and kwargs.get('request_class') and inspect.isclass(kwargs['request_class']):
                request_class = kwargs['request_class'](request=request)
                func(request_class, response)
            elif not response.has_errors:
                func(request, response)
            end_timeout()
            if not response.has_errors:
                run_after(request, response)
            return response

        run_method.requirements = kwargs
        return run_method

    return decorator_func
