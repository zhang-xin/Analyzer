import os
import glob
import json
import configparser


def search(keyword, region):
    ret = []
    config = configparser.ConfigParser()
    config.read('sites-config.ini')
    directory = config['Storage']['directory']

    for source in glob.glob(os.path.join(directory, '*')):
        for f in glob.glob(os.path.join(source, '*.json')):
            j = json.load(open(f))
            if j['Title'].find(keyword.lower()) != -1:
                ret.append(j)

    return ret
