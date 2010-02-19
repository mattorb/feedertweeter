#!/usr/bin/python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template, RequestHandler

from src.utils import pathfix # pyflakes:ignore

import tweepy
from core import feedreader
from core import tweetwriter

from models import Connection

from config import * # pyflakes:ignore

class CreatePage(webapp.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'

        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_CALLBACK)
        
        try:
            request_token = auth.request_token
            auth_url = auth.get_authorization_url()
        except tweepy.TweepError, e:
            # Failed to get a request token
            self.response.out.write(template.render('templates/error.html', {'message': e}))
            return

        # We must store the request token for later use in the callback page.
        connector = Connection(
                token_key = auth.request_token.key,
                token_secret = auth.request_token.secret,
                atomUrl = self.request.get('atomUrl'),
                tweetTemplate = self.request.get('tweetTemplate')
        )
        connector.put()
                
        self.redirect(auth_url)
        
class OAuthCallbackPage(RequestHandler):
    def get(self):
        oauth_token = self.request.get("oauth_token", None)
        oauth_verifier = self.request.get("oauth_verifier", None)
        if oauth_token is None:
            # Invalid request!
            self.response.out.write(template.render('error.html', {
                    'message': 'Missing required parameters!'
            }))
            return

        # Lookup the request token
        connector = Connection.gql("WHERE token_key=:key", key=oauth_token).get()
        if connector is None:
            # We do not seem to have this request token, show an error.
            self.response.out.write(template.render('error.html', {'message': 'Invalid token!'}))
            return

        # Rebuild the auth handler
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_request_token(connector.token_key, connector.token_secret)

        # Fetch the access token
        try:
            auth.get_access_token(oauth_verifier)
            api = tweepy.API(auth_handler=auth, secure=True, retry_count=3)
            connector.twitterName = api.me().screen_name
        except tweepy.TweepError, e:
            # Failed to get access token
            self.response.out.write(template.render('templates/error.html', {'message': e}))
            return

        connector.access_token_key = auth.access_token.key
        connector.access_token_secret = auth.access_token.secret
        connector.verifier = oauth_verifier
        connector.put()
        
        (title, link, id) = feedreader.getLatestEntry(connector.atomUrl)

        tweet = tweetwriter.makeTweet(title, link, connector.tweetTemplate)        
        
        self.response.out.write(template.render('templates/congrats.html', {'tweet': tweet, 'twitterName': connector.twitterName}))
        
    def post(self):
        oauth_token = self.request.get('oauth_token')
        oauth_verifier = self.request.get('oauth_verifier')

        justOne = self.request.get('submitType') == 'Tweet this'
        linkThem = self.request.get('submitType') == 'Tweet this, and tweet future entries!'
        
        connector = Connection.gql("WHERE token_key=:key and verifier=:verifier", key=oauth_token, verifier=oauth_verifier).get()

        (title, link, id) = feedreader.getLatestEntry(connector.atomUrl)

        if justOne:
            if id not in connector.entryIdsThatHaveBeenTweeted:
                tweet = tweetwriter.makeTweet(title, link, connector.tweetTemplate)        

                # Rebuild the auth handler
                auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
                auth.set_access_token(connector.access_token_key, connector.access_token_secret)

                api = tweepy.API(auth_handler=auth, secure=True, retry_count=3)
                api.update_status(tweet)
                
                self.response.out.write(template.render('templates/tweetingout.html', {'tweet' : tweet }))
            else:
                self.response.out.write(template.render('templates/alreadytweeted.html', {}))
        else:
            entryIds = feedreader.getAllEntryIds(connector.atomUrl)
            connector.entryIdsThatHaveBeenTweeted.extend(entryIds)
            connector.enabled = True
            connector.put()
            self.response.out.write(template.render('templates/setupcomplete.html', {}))
    
        connector.enabled = linkThem
        connector.put()
