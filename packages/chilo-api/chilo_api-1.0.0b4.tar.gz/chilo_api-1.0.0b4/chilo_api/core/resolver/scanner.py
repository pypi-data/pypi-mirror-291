from chilo_api.core.exception import ApiException
from chilo_api.core.resolver.importer import ResolverImporter


class ResolverScanner:

    def __init__(self, **kwargs):
        self.importer = ResolverImporter(handlers=kwargs['handlers'])
        self.base_path = self.importer.clean_path(kwargs['base_path'])
        self.has_dynamic_route = False
        self.file_tree_climbed = True
        self.dynamic_parts = {}
        self.import_path = []
        self.__handler_pattern = kwargs['handlers']

    def reset(self):
        self.has_dynamic_route = False
        self.dynamic_parts = {}
        self.file_tree_climbed = True
        self.import_path = []

    def load_importer_files(self):
        self.importer.get_handlers_file_tree()

    def get_endpoint_module(self, request):
        file_path, import_path = self.__get_file_and_import_path(request.path)
        return self.importer.import_module_from_file(file_path, import_path)

    def __get_file_and_import_path(self, request_path):
        split_path = self.__get_request_path_as_list(request_path)
        route_path = self.__get_relative_path(split_path)
        file_path = self.__handler_pattern.split(f'{self.importer.file_separator}*')[0] + self.importer.file_separator + route_path
        import_path = self.__get_import_path(file_path)
        return file_path, import_path

    def __get_request_path_as_list(self, request_path):
        base_path = request_path.replace(self.base_path, '')
        clean_base = self.importer.clean_path(base_path)
        return clean_base.split('/')

    def __get_relative_path(self, split_path):
        file_tree = self.importer.get_handlers_file_tree()
        file_pattern = self.__get_file_pattern()
        self.__get_import_path_file_tree(split_path, 0, file_tree, file_pattern)
        return f'{self.importer.file_separator}'.join(self.import_path)

    def __get_import_path(self, relative_file_path):
        return relative_file_path.replace(self.importer.file_separator, '.').replace('.py', '')

    def __get_file_pattern(self):
        split_pattern = self.__handler_pattern.split(self.importer.file_separator)
        file_pattern = split_pattern[-1]
        return file_pattern

    def __get_import_path_file_tree(self, split_path, split_index, file_tree, file_pattern):
        if split_index < len(split_path):
            route_part = split_path[split_index].replace('-', '_')
            possible_directory, possible_file = self.__get_possible_directory_and_file(route_part, file_pattern)
            if possible_directory in file_tree:
                self.__handle_directory_path_part(possible_directory, split_path, split_index, file_tree, file_pattern)
            elif possible_file in file_tree:
                self.__handle_file_path_part(possible_file, split_path, split_index, file_tree, file_pattern)
            elif file_tree.get('__dynamic_files'):
                self.__handle_dynamic_path_part(split_path, split_index, file_tree, file_pattern)
            else:
                raise ApiException(code=404, message='route not found')

    def __get_possible_directory_and_file(self, route_part, file_pattern):
        possible_directory = f'{route_part}'
        possible_file = file_pattern.replace('*', route_part) if '*' in file_pattern else f'{possible_directory}.py'
        possible_file = '__init__.py' if possible_file == '.py' else possible_file
        return possible_directory, possible_file

    def __handle_directory_path_part(self, possible_directory, split_path, split_index, file_tree, file_pattern):
        self.__append_import_path(possible_directory)
        if split_index+1 < len(split_path):
            file_leaf = self.__determine_which_file_leaf(file_tree, possible_directory)
            self.__get_import_path_file_tree(split_path, split_index+1, file_leaf, file_pattern)
        else:
            index_file = file_pattern.replace('*', possible_directory) if '*' in file_pattern else '__init__.py'
            self.__append_import_path(index_file)

    def __handle_file_path_part(self, possible_file, split_path, split_index, file_tree, file_pattern):
        self.__append_import_path(possible_file)
        file_leaf = self.__determine_which_file_leaf(file_tree, possible_file)
        self.__get_import_path_file_tree(split_path, split_index+1, file_leaf, file_pattern)

    def __handle_dynamic_path_part(self, split_path, split_index, file_tree, file_pattern):
        file_part = list(file_tree['__dynamic_files'])[0]
        self.__append_import_path(file_part)
        if '.py' not in file_part and split_index+1 == len(split_path):  # pragma: no cover
            index_file = file_pattern.replace('*', file_part) if '*' in file_pattern else '__init__.py'
            self.__append_import_path(index_file)
        file_leaf = self.__determine_which_file_leaf(file_tree, file_part)
        self.has_dynamic_route = True
        self.dynamic_parts[split_index] = split_path[split_index]
        self.__get_import_path_file_tree(split_path, split_index+1, file_leaf, file_pattern)

    def __append_import_path(self, path_part):
        if self.file_tree_climbed:
            self.import_path.append(path_part)

    def __determine_which_file_leaf(self, file_tree, file_branch):
        if file_tree.get(file_branch) and file_tree[file_branch] != '*':
            self.file_tree_climbed = True
            return file_tree[file_branch]
        self.file_tree_climbed = False
        return file_tree
