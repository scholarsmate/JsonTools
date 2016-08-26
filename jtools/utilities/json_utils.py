import json
from Table import Table


def load_file_of_json_objects(file_path):
    with open(file_path, 'r') as f:
        return [json.loads(line) for line in f]


def left_join(primary_key_function, file_paths, exclude_columns):
    result = Table(load_file_of_json_objects(file_paths.pop(0)), primary_key_function)
    for file_path in file_paths:
        result = result.left_join(Table(load_file_of_json_objects(file_path), primary_key_function), exclude_columns)
    return result
