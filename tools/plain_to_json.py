#!/usr/bin/env python

import os
import os.path
import glob
import sys
import argparse
import json
import re


def convert_to_json(plain):
    title = ''
    date = ''
    link = ''
    content = ''

    with open(plain, 'r') as f:
        s = f.read()
        result = re.findall(r'Title:\n(.*)\n', s, re.MULTILINE)
        if len(result) != 0:
            title = result[0]
        result = re.findall(r'Date:\n(.*)\n', s, re.MULTILINE)
        if len(result) != 0:
            date = result[0]
        result = re.findall(r'Link:\n(.*)\n', s, re.MULTILINE)
        if len(result) != 0:
            link = result[0]
        result = re.findall(r'Content:\n((?:.|\n)*)\n', s, re.MULTILINE)
        if len(result) != 0:
            content = result[0]

    article = {'Title': title, 'Date': date, 'Link': link, 'Content': content}
    json_name = file + '.json'
    with open(json_name, 'w') as f:
        json.dump(article, f, ensure_ascii=False)


parser = argparse.ArgumentParser(description='convert old plain text articles to json format')
parser.add_argument('directory', action='store', help='where you save your articles')
args = parser.parse_args()

if not os.path.exists(args.directory):
    sys.exit("Error: cannot find directory: %s" % args.directory)

for rss in glob.glob(os.path.join(args.directory, '*')):
    for file in glob.glob(os.path.join(rss, '*')):
        if not file.endswith('.json'):
            if not os.path.exists(file + '.json'):
                convert_to_json(file)
            os.remove(file)
