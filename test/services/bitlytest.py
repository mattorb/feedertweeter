#!/usr/bin/env python
# encoding: utf-8

from test.unit import baseunittest 

from bitly import BitLy

from config import * # pyflakes:ignore

class BitLyTest(baseunittest.GaeBaseUnitTest):
    def testshorten(self): 
        bitly = BitLy(BITLY_LOGIN, BITLY_API_KEY)
        url = 'www.yahoo.com'
        self.assertEquals('http://bit.ly/bxUHoc', bitly.shorten(url)['results']['http://' + url]['shortUrl'])
        self.assertEquals(2, bitly.stats('http://bit.ly/bxUHoc')['results']['userClicks'])
