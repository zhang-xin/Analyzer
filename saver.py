#!/usr/bin/env python

import os.path
import hashlib

from lib import save_file


def _save_to_disk(source, item, directory):
    content = 'Title:\n' + item[0] + '\n'
    content += 'Link:\n' + item[1] + '\n'
    content += 'Date:\n' + item[2] + '\n'
    content += 'Content:\n' + item[3] + '\n'
    folder = os.path.join(directory, source.name)

    h = hashlib.sha1()
    h.update(bytes(item[0], 'utf-8'))
    h.update(bytes(item[1], 'utf-8'))
    h.update(bytes(item[2], 'utf-8'))
    name = h.hexdigest()
    save_file(name, content, folder)


def _save_to_database(source, item, directory):
    pass


_g_save_func = {
    'files': _save_to_disk,
    'database': _save_to_database,
}


def save(*sources, method='files', directory='data'):
    _save = _g_save_func.get(method, _save_to_disk)
    for source in sources:
        source.refresh()
        for item in source.items():
            _save(source, item, directory)


if __name__ == '__main__':
    from reader import RSSReader
    src = RSSReader('ifanr', 'http://www.ifanr.com/feed')
    save(src, method='disk')
