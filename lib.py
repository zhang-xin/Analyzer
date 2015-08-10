#!/usr/bin/env python

import os
import os.path
import json


def save_file(name, content):
    if not os.path.exists(os.path.dirname(name)):
        os.makedirs(os.path.dirname(name))

    json_name = name + '.json'
    if os.path.exists(json_name):
        os.remove(json_name)
    with open(json_name, 'w') as f:
        json.dump(content, f, ensure_ascii=False)


def file_exists(*path):
    file = os.path.join(*path)
    file += '.json'
    return os.path.exists(file)


def path_join(*path):
    return os.path.join(*path)
