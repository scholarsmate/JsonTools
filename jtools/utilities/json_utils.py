import json
from Table import Table
from hdfs_utils import open_for_read


def load_file_of_json_objects(file_path):
    with open_for_read(file_path) as f:
        return [json.loads(line) for line in f]


def read_record(file):
    for line in file:
        yield json.loads(line)


def left_join(primary_key_function, file_paths, exclude_columns, is_primary_key):
    result = Table(load_file_of_json_objects(file_paths.pop(0)), primary_key_function, is_primary_key)
    for file_path in file_paths:
        result = result.left_join(Table(load_file_of_json_objects(file_path), primary_key_function), exclude_columns)
    return result
