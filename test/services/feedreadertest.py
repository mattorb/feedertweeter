#!/usr/bin/env python
# encoding: utf-8

from test.unit import baseunittest #todo: split out base integration test when something is diff.
from core import feedreader

class RetrieverTest(baseunittest.GaeBaseUnitTest):
    def testfetchparse(self): 
        (title, link, id) = feedreader.getLatestEntry('http://netsmith.blogspot.com/feeds/posts/default')

        self.assertNotNull(title)
        self.assertNotNull(link)
        self.assertNotNull(id)
