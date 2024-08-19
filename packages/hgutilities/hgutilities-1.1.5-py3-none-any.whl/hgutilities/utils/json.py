from json import load as json_load
from json import dumps as json_dumps
import re

import numpy as np


def dumps(input_json, indent=2):
    json_string = compress_bottom_layer_lists(json_dumps(
        input_json,
        default=numpy_encoder,
        indent=indent))
    return json_string

def dump(input_json, file, indent=2):
    json_string = dumps(input_json, indent)
    file.writelines(json_string)

def load(file):
    contents = json_load(file)
    return contents

def numpy_encoder(obj):
    if isinstance(obj, np.ndarray):
        return convert_to_int_if_possible(obj.tolist())
    raise TypeError(f"Object of type {type(obj).__name__}"
                    "is not JSON serializable")

def convert_to_int_if_possible(data):
    if isinstance(data, list):
        return [convert_to_int_if_possible(item) for item in data]
    elif isinstance(data, float) and data.is_integer():
        return int(data)
    else:
        return data

def compress_bottom_layer_lists(json_str):
    compressed_str = pattern.sub(lambda m: '[' + m.group(1)
                                 .replace('\n', ' ')
                                 .replace('  ', '') + ']', json_str)
    return compressed_str

pattern = re.compile(r'\[\n\s+([^\[\]]+?)\n\s+\]')
