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

            content = {'Title': item[0], 'Link': item[1], 'Date': item[2], 'Language': item[3], 'Content': doc}
            _save(name, content, path_join(directory, source.name))


if __name__ == '__main__':
    from reader import RSSReader
    src = RSSReader('ifanr', 'http://www.ifanr.com/feed', 'chinese')
    save(src, method='disk')
