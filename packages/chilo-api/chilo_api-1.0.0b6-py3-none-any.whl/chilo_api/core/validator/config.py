class ConfigValidator:

    @staticmethod
    def validate(**kwargs):
        if not kwargs.get('base_path') or not isinstance(kwargs.get('base_path'), str):
            raise RuntimeError('base_path string is required')
        if not kwargs.get('handlers') or not isinstance(kwargs.get('handlers'), str):
            raise RuntimeError('handlers is required; must be glob pattern string {route: file_path}')
        if kwargs.get('openapi') and not isinstance(kwargs.get('openapi'), str):
            raise RuntimeError('schema should either be file path string')
        if kwargs.get('openapi_validate_request') and not isinstance(kwargs.get('openapi_validate_request'), bool):
            raise RuntimeError('openapi_validate_request should be a boolean')
        if kwargs.get('openapi_validate_request') and kwargs.get('openapi') is None:
            raise RuntimeError('schema is required to use openapi_validate_request')
        if kwargs.get('openapi_validate_response') and not isinstance(kwargs.get('openapi_validate_response'), bool):
            raise RuntimeError('openapi_validate_response should be a boolean')
        if kwargs.get('cache_size') and not isinstance(kwargs.get('cache_size'), int) and kwargs.get('cache_size') is not None:
            raise RuntimeError('cache_size should be an int (0 for unlimited size) or None (to disable route caching)')
        if kwargs.get('cache_mode') and kwargs['cache_mode'] not in ('all', 'static-only', 'dynamic-only'):
            raise RuntimeError('cache_mode should be a string of the one of the following values: all, static-only, dynamic-only')
        if kwargs.get('verbose') and not isinstance(kwargs.get('verbose'), bool):
            raise RuntimeError('verbose should be a boolean')
