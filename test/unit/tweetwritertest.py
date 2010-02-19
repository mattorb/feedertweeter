#!/usr/bin/env python
# encoding: utf-8

from test.unit import baseunittest
from core import tweetwriter

class TweetMakerTest(baseunittest.GaeBaseUnitTest):
    def testMakeTweet(self): 
        (title, link) = ('My blog entry', 'http://www.blogspot.com')
        
        tweet = tweetwriter.makeTweet(title, link, 'New Blog Entry: "{title}" {link}', shortener=None)
        
        self.assertEquals('New Blog Entry: "%s" %s' % (title, link), tweet)
    #add tests for truncating title with ... ensuring link is always there, etc
    
    def testMakeTweetWithShortener(self): 
        (title, link) = ('My blog entry', 'http://www.blogspot.com')
        
        tweet = tweetwriter.makeTweet(title, link, 'New Blog Entry: "{title}" {link}', shortener = lambda x: 'blahblah')
        
        self.assertEquals('New Blog Entry: "%s" blahblah' % title, tweet)
