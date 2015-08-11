#!/usr/bin/env python


import configparser

import feedparser
import requests
from bs4 import BeautifulSoup
import dateutil.parser
import dateutil.tz


def _cnbeta_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding=r.encoding)

        content = soup.find('div', class_='content')
        return content.get_text()
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None


def _ifanr_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding=r.encoding)

        content = soup.find('div', itemprop='articleBody')
        return content.get_text()
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None


def _36kr_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding=r.encoding)

        content = soup.find('section', class_='article')
        return content.get_text()
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None


_g_extractor = {
    'cnbeta': _cnbeta_extractor,
    'ifanr': _ifanr_extractor,
    '36kr': _36kr_extractor,
}


class RSSReader:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.error = False
        self._feed = None
        self.extractor = _g_extractor.get(self.name, None)

    def refresh(self, timeout=30):
        if self.extractor is None:
            self.error = True
            return
        try:
            self.error = False
            r = requests.get(self.url, timeout=timeout)
            if r.status_code != 200:
                self.error = True
                return
            r.encoding = 'utf-8'
            self._feed = feedparser.parse(r.text)
        except requests.exceptions.RequestException:
            self.error = True
        except ConnectionError:
            self.error = True

    def items(self):
        if self.error:
            raise StopIteration()
        for item in self._feed.entries:
            yield (item.title, item.link, item.published)

    def get_article(self, link):
        if self.extractor is None:
            self.error = True
            return None
        return self.extractor(link)

    @staticmethod
    def time_earlier(time1, time2):
        last = dateutil.parser.parse(time1)
        now = dateutil.parser.parse(time2)
        return last < now


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('sites-config.ini')
    for site, rss_url in config['RSS'].items():
        print(site, rss_url)
        reader = RSSReader(site, rss_url)
        reader.refresh()
        s = "Wed, 29 Jul 2015 03:17:56 GMT"
        for it in reader.items():
            print('title:\n' + it[0])
            print('link:\n' + it[1])
            print('date:\n' + it[2])
            content = reader.get_article(it[1])
            if content is not None:
                print('content:\n' + content)
            if reader.time_earlier(s, it[2]):
                print('earlier')
            else:
                print('later')
