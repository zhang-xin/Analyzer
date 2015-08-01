# Analyzer for Contents from Web Sources

Far far away from stable.

## How to Use

Code is written in Python 3.

Windows is not supported to use background download service.

### Install

```
For Python 3.4:
$ pyvenv venv
For earlier version of Python, install virtualenv from pip or distribution repository, then:
$ virtualenv venv

$ source venv/bin/activate
$ pip install -r requirements.txt
```

Then you're ready to use it.

Quit from this virtual environment:

```
$ deactivate
```

## Tasks

- [x] Background service for continuously downloading articles from RSS
- [ ] Add more RSS sources as not only technology sources
- [ ] Extract chinese words from articles
- [ ] Download theses of interests, articles on the web
- [ ] Extract contents from PDF
- [ ] Unify saved document format
- [ ] Analyze contents of articles
    - [ ] Relationship
    - [ ] Clusters: by companies, software/hardware, sources, contents
    - [ ] Trends
    - [ ] Which source likes which topic
- [ ] Run analyze on contents from other datasets
- [ ] Database support
- [ ] Web UI or GUI to show the results
