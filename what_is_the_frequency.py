#!/usr/bin/env python

import glob
import json
import os.path
import pprint
import argparse
import configparser

import nltk
import jieba
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer


def keyword_frequency(keyword, directory):
    freq_table = {}

    for source in glob.glob(os.path.join(directory, '*')):
        words = ''
        vect = CountVectorizer(ngram_range=(1, 3))
        analyzer = vect.build_analyzer()

        for f in glob.glob(os.path.join(source, '*.json')):
            j = json.load(open(f))
            if j['Language'] == 'chinese':
                words += ' '.join(jieba.cut(j['Title']))
                words += ' '.join(jieba.cut(j['Content']))
            elif j['Language'] == 'english':
                words += j['Title']
                words += j['Content']
        ngram_query = analyzer(words)
        fdist = nltk.FreqDist(ngram_query)
        freq = fdist.freq(keyword.lower())
        freq_table[os.path.basename(source)] = freq

    pprint.pprint(freq_table)

    sorted_list = sorted(freq_table, key=freq_table.get, reverse=True)
    print('=================')
    print("%s loves %s most." % (sorted_list[0], keyword))

    plt.bar(range(len(freq_table)), freq_table.values(), align="center")
    plt.xticks(range(len(freq_table)), list(freq_table.keys()))
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyzer')
    parser.add_argument('-c', '--config', action='store', default='sites-config.ini', dest='config', help='config file')
    parser.add_argument('keyword', action='store', help='keyword to check frequency')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    dire = config['Storage']['directory']

    keyword_frequency(args.keyword, dire)
