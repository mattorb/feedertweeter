#!/usr/bin/env python
# encoding: utf-8

from test.unit import baseunittest #todo: split out base integration test when something is diff.

import tweepy

class TweepyTest(baseunittest.GaeBaseUnitTest):
    def testtweepyapi(self): 
        self.assertNotNull(tweepy.api.rate_limit_status())
        self.assertNotNull([x.text for x in tweepy.api.public_timeline()])
