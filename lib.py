#!/usr/bin/env python

import os
import os.path


def save_file(name, content):
    if not os.path.exists(os.path.dirname(name)):
        os.makedirs(os.path.dirname(name))

    if os.path.exists(name):
        os.remove(name)
    with open(name, 'w') as f:
        f.write(content)


def file_exists(*path):
    file = os.path.join(*path)
    return os.path.exists(file)


def path_join(*path):
    return os.path.join(*path)
