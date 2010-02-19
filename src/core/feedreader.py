#!/usr/bin/env python
# encoding: utf-8

from StringIO import StringIO

from google.appengine.api import urlfetch

import feedparser

def getLatestEntry(url):
    content = urlfetch.fetch(url).content
    d = feedparser.parse(StringIO(content))

    return (d['entries'][0]['title'], d['entries'][0].link, d['entries'][0].id)

def getAllEntryIds(url):
    content = urlfetch.fetch(url).content
    d = feedparser.parse(StringIO(content))

    return [entry.id for entry in d['entries']]
