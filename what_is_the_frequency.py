#!/usr/bin/env python

import glob
import json
import os.path
import pprint
import argparse
import configparser

import nltk
import jieba


def keyword_frequency(keyword, directory):
    freq_table = {}

    for source in glob.glob(os.path.join(directory, '*')):
        words = []
        for f in glob.glob(os.path.join(source, '*.json')):
            j = json.load(open(f))
            if j['Language'] == 'chinese':
                words.extend(jieba.cut(j['Title']))
                words.extend(jieba.cut(j['Content']))
            elif j['Language'] == 'english':
                words.extend(nltk.word_tokenize(j['Title']))
                words.extend(nltk.word_tokenize(j['Content']))
        fdist = nltk.FreqDist(word.lower() for word in words)
        freq = fdist.freq(keyword)
        freq_table[os.path.basename(source)] = freq

    pprint.pprint(freq_table)

    sorted_list = sorted(freq_table, key=freq_table.get, reverse=True)
    print('=================')
    print("%s loves %s most." % (sorted_list[0], keyword))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyzer')
    parser.add_argument('-c', '--config', action='store', default='sites-config.ini', dest='config', help='config file')
    parser.add_argument('keyword', action='store', help='keyword to check frequency')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    dire = config['Storage']['directory']

    keyword_frequency(args.keyword.lower(), dire)
