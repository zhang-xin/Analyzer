#!/usr/bin/env python

import os
import os.path
import shutil
import tempfile


def save_file(name, content):
    if not os.path.exists(os.path.dirname(name)):
        os.makedirs(os.path.dirname(name))

    f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    f.write(content)
    f.close()
    if os.path.exists(name):
        os.remove(name)
    shutil.move(f.name, name)


def file_exists(*path):
    file = os.path.join(*path)
    return os.path.exists(file)


def path_join(*path):
    return os.path.join(*path)
