import traceback

from icecream import ic


class CommonLogger:

    def __init__(self, **kwargs):
        self.__log_level = kwargs.get('level', 'INFO')
        self.log_levels = {'DEBUG': 1, 'INFO': 2, 'WARN': 3, 'ERROR': 4, 'CRITICAL': 5, 'NOTSET': 99}
        self.__validate_configs()

    def log(self, *args, **kwargs):
        log = {'level': kwargs.get('level', 'INFO'), 'log': kwargs.get('log', args)}
        if self.__should_log(log['level']):
            self.__log(**log)

    def __validate_configs(self):
        if self.__log_level not in self.log_levels.keys():
            raise RuntimeError(f'level argument must be {",".join(self.log_levels.keys())}; recieved: {self.__log_level}')

    def __should_log(self, level):
        current_log_level = self.log_levels[level]
        log_level_setting = self.log_levels[self.__log_level]
        return current_log_level >= log_level_setting

    def __get_traceback(self):
        trace = traceback.format_exc()
        if str(trace) != 'NoneType: None\n':
            return trace
        return ''

    def __log(self, **kwargs):
        trace = self.__get_traceback()
        prefix = f"{trace}\n{kwargs['level']} | "
        log = kwargs['log']
        ic.configureOutput(prefix=prefix)
        ic(log)
