import json

from Table import Table
from hdfs_utils import open_for_read


def load_file_of_json_objects(file_path):
    with open_for_read(file_path) as f:
        return [json.loads(line) for line in f]


def read_record(file):
    for line in file:
        yield json.loads(line)


def flatten_json(rec, delim):
    flat_map = {}
    for i in rec.keys():
        if isinstance(rec[i], dict):
            nested = flatten_json(rec[i], delim)
            for j in nested.keys():
                flat_map[i + delim + j] = nested[j]
        else:
            flat_map[i] = rec[i]
    return flat_map


def left_join(primary_key_function, file_paths, exclude_columns, is_primary_key):
    result = Table(load_file_of_json_objects(file_paths.pop(0)), primary_key_function, is_primary_key)
    for file_path in file_paths:
        result = result.left_join(Table(load_file_of_json_objects(file_path), primary_key_function), exclude_columns)
    return result
