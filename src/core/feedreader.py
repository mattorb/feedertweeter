#!/usr/bin/env python
# encoding: utf-8

import feedparser

def getLatestEntry(url):
    d = feedparser.parse(url)
    return (d['entries'][0]['title'], d['entries'][0].link, d['entries'][0].id)

def getAllEntryIds(url):
    d = feedparser.parse(url)

    return [entry.id for entry in d['entries']]
