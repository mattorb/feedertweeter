#!/usr/bin/python
# -*- coding: utf-8 -*-

from bitly import BitLy

from config import * # pyflakes:ignore

def buildbitlyshortener():
    bitly = BitLy(BITLY_LOGIN, BITLY_API_KEY)
    return lambda x:bitly.shorten(x.replace('http://', ''))['results']['http://' + x.replace('http://', '')]['shortUrl']

bitlyshortener = buildbitlyshortener()

def makeTweet(title, link, template, shortener=bitlyshortener):
    if shortener:
        url = shortener(link)
    else:
        url = link
    
    return template.replace('{title}', title).replace('{link}', url)
    
