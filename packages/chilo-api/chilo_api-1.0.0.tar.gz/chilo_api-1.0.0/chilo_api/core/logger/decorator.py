from chilo_api import logger


def log(**settings):
    '''
    A decorator to make logging simplier and DRY'er; will capture all args, kwargs and ouput of decorated function/method

    level: str, enum(DEBUG, INFO, WARN, ERROR)
        The log level to log (default is INFO)
    condition: callable, optional
        A callable function which will determine if log should happen; callable must return truth-y/false-y value
    '''
    def decorator_func(func):
        captured = {'arguments': {}, 'result': None}

        def run_func(*args, **kwargs):
            captured['arguments']['args'] = list(args)
            captured['arguments']['kwargs'] = kwargs
            captured['result'] = func(*args, **kwargs)
            if settings.get('condition') and callable(settings['condition']):
                if settings['condition'](*args, **kwargs):
                    logger.log(level=settings.get('level', 'INFO'), log=captured)
            else:
                logger.log(level=settings.get('level', 'INFO'), log=captured)
            return captured['result']

        return run_func

    return decorator_func
