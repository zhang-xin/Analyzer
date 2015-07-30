#!/usr/bin/env python

import argparse
import configparser

import reader
import saver


def main():
    parser = argparse.ArgumentParser(description='Analyzer')
    parser.add_argument('-c', '--config', action='store', default='sites-config.ini', dest='config', help='config file')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    readers = []
    for site, rss_url in config['RSS'].items():
        readers.append(reader.RSSReader(site, rss_url))

    saver.save(*readers)


if __name__ == "__main__":
    main()
