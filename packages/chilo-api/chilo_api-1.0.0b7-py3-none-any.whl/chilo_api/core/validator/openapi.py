from openapi_spec_validator import validate

from chilo_api.core.resolver.importer import ResolverImporter
from chilo_api.core.validator.schema import Schema


class OpenApiValidator:
    SUPPORTED_METHODS = ['any', 'delete', 'get', 'patch', 'post', 'put']

    def __init__(self, **kwargs):
        self.__handlers = kwargs['handlers']
        self.__base_path = kwargs.get('base_path', '')
        self.__openapi_validate_request = kwargs.get('openapi_validate_request', False)
        self.__openapi_validate_spec = kwargs.get('openapi_validate_spec', True)
        self.__schema = Schema(**kwargs)
        self.__importer = ResolverImporter(handlers=kwargs['handlers'])

    def validate_openapi(self):
        self.__schema.load_schema_file()
        if not self.__schema.spec:
            return
        if self.__openapi_validate_spec:
            self.__validate_openapi_spec()
        module_dict = self.__get_module_dict()
        self.__verify_required_body_exist_in_openapi(module_dict)
        self.__verify_required_response_exist_in_openapi(module_dict)
        if self.__openapi_validate_request:
            self.__verify_routes_method_exist_in_openapi(module_dict)

    def __validate_openapi_spec(self):
        try:
            validate(self.__schema.spec)
        except Exception as openapi_error:
            raise RuntimeError('there was a problem with your openapi schema; see above') from openapi_error

    def __get_module_dict(self):
        route_list = self.__importer.get_file_list()
        sep = self.__importer.file_separator
        modules = self.__get_modules_from_routes(sep, route_list)
        return modules

    def __get_modules_from_routes(self, sep, route_list):
        modules = {}
        for route_item in route_list:
            file_path = self.__handlers.split(f'{sep}*')[0] + route_item
            import_path = file_path.replace(sep, '.').replace('.py', '')
            file_route = self.__clean_up_route(route_item)
            module = self.__importer.import_module_from_file(file_path, import_path)
            self.__add_routes_and_methods_to_modules(file_route, modules,  module)
        return modules

    def __add_routes_and_methods_to_modules(self, file_route, modules,  module):
        for method in dir(module):
            if method in self.SUPPORTED_METHODS:
                route = self.__determine_route(file_route, getattr(module, method))
                base = self.__base_path.strip('/')
                path = f'{base}{route}'.strip('/')
                route_path = f'/{path}'
                if not modules.get(route_path):
                    modules[route_path] = {'methods': []}
                modules[route_path]['methods'].append(method)
                modules[route_path]['request_schemas'] = self.__get_required_body_schemas(module)
                modules[route_path]['response_schemas'] = self.__get_required_response_schemas(module)

    def __clean_up_route(self, route_item):
        route_no_extension = route_item.replace('.py', '').replace('__init__', '')
        route_forward_slash = route_no_extension.replace(self.__importer.file_separator, '/')
        route_hyphonated = route_forward_slash.replace('_', '-')
        route_dynamic = self.__replace_dynamic_files_with_variales(route_hyphonated)
        route = route_dynamic.strip('/')
        return route

    def __replace_dynamic_files_with_variales(self, route_hyphonated):
        replaced = []
        for route in route_hyphonated.split('/'):
            route_variable = route
            if route.startswith('-'):
                dynamic_hyphonated = route.replace('-', '', 1)
                dynamic_file = dynamic_hyphonated.replace('-', '_')
                route_variable = f'{{{dynamic_file}}}'
            replaced.append(route_variable)
        return '/'.join(replaced)

    def __determine_route(self, file_route, module_method):
        requirements = getattr(module_method, 'requirements', {})
        if requirements.get('required_route'):
            required_route = requirements['required_route'].strip('/')
            return f'/{required_route}'
        return f'/{file_route}'

    def __get_required_body_schemas(self, module):
        schemas = []
        for method in dir(module):
            if method in self.SUPPORTED_METHODS:
                module_method = getattr(module, method)
                requirements = getattr(module_method, 'requirements', {})
                if requirements.get('required_body') and isinstance(requirements['required_body'], str):
                    schemas.append(requirements['required_body'])
        return schemas

    def __get_required_response_schemas(self, module):
        schemas = []
        for method in dir(module):
            if method in self.SUPPORTED_METHODS:
                module_method = getattr(module, method)
                requirements = getattr(module_method, 'requirements', {})
                if requirements.get('required_response') and isinstance(requirements['required_response'], str):
                    schemas.append(requirements['required_response'])
        return schemas

    def __verify_routes_method_exist_in_openapi(self, module_dict):
        for route in module_dict.keys():
            if not self.__schema.paths.get(route):
                raise RuntimeError(f'openapi_validate_request is enabled and route {route} does not exist in openapi')
            for method in module_dict[route]['methods']:
                if not self.__schema.paths[route].get(method):
                    raise RuntimeError(f'openapi_validate_request is enabled and method {method} in route {route} does not exist in openapi')

    def __verify_required_body_exist_in_openapi(self, module_dict):
        for route, values in module_dict.items():
            for schema in values.get('request_schemas', []):
                if not self.__schema.spec['components']['schemas'].get(schema):
                    raise RuntimeError(f'required_body schema {schema} from {route} not found in openapi')

    def __verify_required_response_exist_in_openapi(self, module_dict):
        for route, values in module_dict.items():
            for schema in values.get('response_schemas', []):
                if not self.__schema.spec['components']['schemas'].get(schema):
                    raise RuntimeError(f'required_response schema {schema} from {route} not found in openapi')
