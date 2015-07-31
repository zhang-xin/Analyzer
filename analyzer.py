#!/usr/bin/env python

import argparse
import configparser
import sys
import os.path
import logging
from logging.handlers import SysLogHandler
import time

from service import find_syslog, Service

import reader
import saver


class DownloadService(Service):
    def __init__(self, *args, **kwargs):
        super(DownloadService, self).__init__(*args, **kwargs)
        self.logger.addHandler(SysLogHandler(address=find_syslog(),
                                             facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.INFO)
        self.readers = []
        self.method = 'disk'
        self.directory = 'data'
        self.time_interval = 15

    def run(self):
        self.logger.info("Analyzer: start analyzer download service")
        last = 0
        while not self.got_sigterm():
            if time.time() > last + self.time_interval * 60:
                self.logger.info("Analyzer: check latest articles")
                saver.save(*self.readers, method=self.method, directory=self.directory)
                last = time.time()
            time.sleep(5)
        else:
            self.logger.info("Analyzer: stop analyzer download service")

    def set_parameters(self, readers, method, directory, time_interval):
        self.readers = readers
        self.method = method
        self.directory = directory
        self.time_interval = time_interval


def main():
    parser = argparse.ArgumentParser(description='Analyzer')
    parser.add_argument('-c', '--config', action='store', default='sites-config.ini', dest='config', help='config file')
    parser.add_argument('--oneshot', action='store_true', dest='oneshot', help='download current articles then exit')
    parser.add_argument('-t', '--time_interval', action='store', type=int, default=15, dest='time_interval',
                        help='time interval to check new content (unit in minute, default 15)')
    parser.add_argument('command', action='store', help='start|stop|status')
    args = parser.parse_args()

    if not os.path.exists(args.config):
        sys.exit('Error: config file not found!')

    config = configparser.ConfigParser()
    config.read(args.config)

    readers = []

    for site, rss_url in config['RSS'].items():
        readers.append(reader.RSSReader(site, rss_url))

    try:
        method = config['Storage']['method']
        directory = os.path.abspath(config['Storage']['directory'])
        if method != "disk" and method != 'database':
            sys.exit('Error: storage method invalid!')
    except KeyError:
        sys.exit('Error: storage parameters missing!')

    service = DownloadService('AnalyzerDownloadService', pid_dir='/tmp')

    if args.command == 'start':
        if args.oneshot:
            saver.save(*readers, method=method, directory=directory)
            return

        service.set_parameters(readers, method, directory, args.time_interval)
        service.start()
    elif args.command == 'stop':
        service.stop()
    elif args.command == 'status':
        if service.is_running():
            print("Service is running.")
        else:
            print("Service is not running.")
    else:
        sys.exit('Error: Unknown command "%s".' % args.command)


if __name__ == "__main__":
    main()
