#!/usr/bin/env python

import os
import os.path
import glob
import argparse
import json
import configparser


def add_language_entry(file, language):
    print(file, language)
    with open(file, 'r') as f:
        j = json.load(f)
    if j.get('Language', None) is None:
        j['Language'] = language
        os.remove(file)
        json.dump(j, open(file, 'w'), ensure_ascii=False)

parser = argparse.ArgumentParser(description='add language entry')
parser.add_argument('-c', '--config', action='store', default='sites-config.ini', dest='config', help='config file')
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.config)

for rss in glob.glob(os.path.join(config['Storage']['directory'], '*')):
    for file in glob.glob(os.path.join(rss, '*.json')):
        _, lang = config['RSS'][os.path.basename(rss)].split(' ')
        add_language_entry(file, lang)
