class InputArguments:

    def __init__(self, api, args):
        self.__base = api.base_path
        self.__handlers = api.handlers
        self.__output = args.output or api.handlers
        self.__formats = args.format or 'yml'
        self.__delete = args.delete or False

    @property
    def base(self):
        return self.__base

    @property
    def handlers(self):
        return self.__handlers

    @property
    def output(self):
        return self.__output

    @property
    def formats(self):
        return self.__formats.split(',')

    @property
    def delete(self):
        return self.__delete
