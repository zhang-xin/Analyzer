#!/usr/bin/env python


import feedparser
import configparser
import requests
from bs4 import BeautifulSoup


def cnbeta_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding=r.encoding)

        content = soup.find('div', class_='content')
        return content.get_text()
    except TimeoutError:
        return None


def ifanr_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding=r.encoding)

        content = soup.find('div', itemprop='articleBody')
        return content.get_text()
    except TimeoutError:
        return None


g_extractor = {
    'cnbeta': cnbeta_extractor,
    'ifanr': ifanr_extractor,
}


class RSSReader:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.error = False
        self._feed = None

        self.extractor = g_extractor.get(self.name, None)
        if self.extractor is None:
            self.error = True

        self.refresh()

    def refresh(self, timeout=30):
        try:
            r = requests.get(self.url, timeout=timeout)
            if r.status_code != 200:
                self.error = True
                return
            self._feed = feedparser.parse(r.text)
        except TimeoutError:
            self.error = True

    def items(self):
        for item in self._feed.entries:
            yield (item.title, item.link, self.extractor(item.link))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('sites-config.ini')
    for sect in config.sections():
        print(sect)
        for site, rss_url in config[sect].items():
            print(site, rss_url)
            reader = RSSReader(site, rss_url)
            for it in reader.items():
                print(it[0])
