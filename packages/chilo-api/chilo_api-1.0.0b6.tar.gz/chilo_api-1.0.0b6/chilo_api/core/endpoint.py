from chilo_api.core.exception import ApiException
from chilo_api.core import logger


class Endpoint:
    SUPPORTED_METHODS = ['any', 'delete', 'get', 'patch', 'post', 'put']

    def __init__(self, module, method):
        self.__module = module
        self.__method = method
        self.__module_method = None if method in {'options', 'head'} else getattr(module, method)
        self.__requirements = {} if method in {'options', 'head'} else getattr(self.__module_method, 'requirements', {})

    @property
    def module(self):
        return self.__module

    @property
    def has_requirements(self):
        return bool(self.__requirements)

    @property
    def requirements(self):
        return self.__requirements

    @property
    def requires_auth(self):
        return self.__requirements.get('auth_required')

    @property
    def has_required_response(self):
        return bool(self.__requirements.get('required_response'))

    @property
    def has_required_route(self):
        return bool(self.__requirements.get('required_route'))

    @property
    def required_route(self):
        return self.__requirements.get('required_route', '')

    def run(self, request, response):
        if self.__method == 'options':
            return self.__run_options(request, response)
        elif self.__method == 'head':
            return self.__run_head(request, response)
        return self.__module_method(request, response)

    def __run_options(self, _, response):
        methods, headers = self.__get_module_methods_and_headers()
        response.headers = ('Accept-Encoding', '*')
        response.headers = ('Access-Control-Request-Method', ','.join(methods))
        response.headers = ('Access-Control-Request-Headers', ','.join(headers))
        return response

    def __run_head(self, request, response):
        try:
            method_func = getattr(self.__module, 'get')
            method_func(request, response)
            response.body = None
            return response
        except Exception as error:  # pragma: no cover
            logger.log(level='ERROR', log=error)
            raise ApiException(code=403, message='method not allowed')

    def __get_module_methods_and_headers(self):
        methods = []
        headers = ['content-type']
        for method in dir(self.__module):
            if method.lower() in self.SUPPORTED_METHODS:
                methods.append(method.upper())
                method_func = getattr(self.__module, method)
                method_requirements = getattr(method_func, 'requirements', {})
                available_headers = method_requirements.get('available_headers', [])
                required_headers = method_requirements.get('required_headers', [])
                headers.extend(available_headers + required_headers)
        return methods, headers
