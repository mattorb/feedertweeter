#!/usr/bin/env python
# encoding: utf-8
from google.appengine.ext import webapp

import logging
import models
from core import feedreader
from core import tweetwriter
import tweepy

from src.utils import pathfix # pyflakes:ignore

from config import * # pyflakes:ignore


class Poller(webapp.RequestHandler):
    def get(self):
        enabledConnections = models.Connection.gql('where enabled = True')
        logging.info('starting check for new entries')
        
        for connector in enabledConnections:
            if connector.access_token_key and connector.access_token_secret:
                try:
                    (title, link, id) = feedreader.getLatestEntry(connector.atomUrl)
                    logging.debug('latest entry for %s is %s (%s)' % (connector.atomUrl, id, title))
#                    logging.debug('entries that have been tweeted are: %s' % connector.entryIdsThatHaveBeenTweeted)
                    
                    if len(connector.entryIdsThatHaveBeenTweeted) == 0:
                        #if none have been done, mark all done -- don't want to blast
                        entryIds = feedreader.getAllEntryIds(connector.atomUrl)
                        connector.entryIdsThatHaveBeenTweeted.extend(entryIds)
                        connector.put()
                    else:
                        if id not in connector.entryIdsThatHaveBeenTweeted:
                            logging.info('Posting entry with id %s - %s' % (id, link))
                            tweet = tweetwriter.makeTweet(title, link, connector.tweetTemplate)
                            
                            auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
                            auth.set_access_token(connector.access_token_key, connector.access_token_secret)

                            api = tweepy.API(auth_handler=auth, secure=True, retry_count=3)
                            api.update_status(tweet)

                            connector.entryIdsThatHaveBeenTweeted.append(id)
                            connector.put()
                        else:
                            pass # the latest entry has been tweeted already
                except Exception, e:
                    logging.error(e)
            else:
                pass
                # no access/authorization yet