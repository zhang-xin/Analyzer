#!/usr/bin/env python

import hashlib

from lib import save_file, file_exists, path_join


def _save_to_disk(name, content, directory):
    name = path_join(directory, name)
    save_file(name, content)


def _save_to_database(name, content, directory):
    pass


_g_save_func = {
    'disk': _save_to_disk,
    'database': _save_to_database,
}


def save(*sources, method='disk', directory='data'):
    _save = _g_save_func.get(method, _save_to_disk)
    for source in sources:
        source.refresh()
        for item in source.items():
            h = hashlib.sha1()
            h.update(bytes(item[0], 'utf-8'))
            h.update(bytes(item[1], 'utf-8'))
            h.update(bytes(item[2], 'utf-8'))
            name = h.hexdigest()
            if file_exists(directory, source.name, name):
                continue

            doc = source.get_article(item[1])
            if doc is None:
                continue

            content = 'Title:\n' + item[0] + '\n'
            content += 'Link:\n' + item[1] + '\n'
            content += 'Date:\n' + item[2] + '\n'
            content += 'Content:\n' + doc + '\n'
            _save(name, content, path_join(directory, source.name))


if __name__ == '__main__':
    from reader import RSSReader
    src = RSSReader('ifanr', 'http://www.ifanr.com/feed')
    save(src, method='disk')
