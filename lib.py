#!/usr/bin/env python

import os
import os.path
import shutil
import tempfile


def save_file(name, content, path):
    if not os.path.exists(path):
        os.makedirs(path)

    f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    f.write(content)
    f.close()
    new_file = os.path.join(path, name)
    if os.path.exists(new_file):
        os.remove(new_file)
    shutil.move(f.name, new_file)
