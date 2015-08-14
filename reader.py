#!/usr/bin/env python


import configparser
import socket

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

        content = soup.find('div', class_='introduction')
        if content is not None:
            text = content.get_text()
        else:
            text = ""
        content = soup.find('div', class_='content')
        if content is not None:
            text += content.get_text()
        else:
            text += ""
        return text
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None
    except socket.timeout:
        return None


def _ifanr_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding=r.encoding)

        content = soup.find('div', itemprop='articleBody')
        if content is not None:
            return content.get_text()
        else:
            return ""
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None
    except socket.timeout:
        return None


def _36kr_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding=r.encoding)

        content = soup.find('section', class_='article')
        if content is not None:
            return content.get_text()
        else:
            return ""
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None
    except socket.timeout:
        return None


def _tongrenyuye_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding=r.encoding)

        content = soup.find('div', class_='post-content clearfix')
        if content is not None:
            return content.get_text()
        else:
            return ""
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None
    except socket.timeout:
        return None


def _linuxtoy_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding=r.encoding)

        content = soup.find('div', class_='post-description')
        if content is not None:
            return content.get_text()
        else:
            return ""
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None
    except socket.timeout:
        return None


def _paulgraham_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')

        content = soup.find('table', width=True)
        if content is not None:
            return content.get_text()
        else:
            return ""
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None
    except socket.timeout:
        return None


def _buxulianxiang_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        content = soup.find('div', class_='entry')
        if content is not None:
            return content.get_text()
        else:
            return ""
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None
    except socket.timeout:
        return None


def _chedanji_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        content = soup.find('div', class_='entry-content')
        if content is not None:
            return content.get_text()
        else:
            return ""
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None
    except socket.timeout:
        return None


def _ruanyifeng_extractor(url, timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        content = soup.find('div', id='main-content')
        if content is not None:
            return content.get_text()
        else:
            return ""
    except requests.exceptions.RequestException:
        return None
    except ConnectionError:
        return None
    except socket.timeout:
        return None


_g_extractor = {
    'cnbeta': _cnbeta_extractor,
    'ifanr': _ifanr_extractor,
    '36kr': _36kr_extractor,
    '学而时嘻之': _tongrenyuye_extractor,
    'linuxtoy': _linuxtoy_extractor,
    'paulgraham': _paulgraham_extractor,
    '不许联想': _buxulianxiang_extractor,
    '扯氮集': _chedanji_extractor,
    '阮一峰的网络日志': _ruanyifeng_extractor,
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
        except socket.timeout:
            self.error = True

    def items(self):
        if self.error:
            raise StopIteration()
        for item in self._feed.entries:
            date = item.get('published')
            if date is None:
                date = item.get('updated', default='')
            yield (item.title, item.link, date)

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
            c = reader.get_article(it[1])
            if c is not None:
                print('content:\n' + c)
            if reader.time_earlier(s, it[2]):
                print('earlier')
            else:
                print('later')
