#!/usr/bin/env python
# encoding: utf-8

from google.appengine.ext import db

class BaseModel(db.Model):                           
    stamp = db.DateTimeProperty(auto_now_add=True)

class Connection(BaseModel):
    atomUrl = db.StringProperty()
    tweetTemplate = db.StringProperty()
    entryIdsThatHaveBeenTweeted = db.StringListProperty()
    twitterName = db.StringProperty()

    token_key = db.StringProperty(required=True)
    token_secret = db.StringProperty(required=True)
    access_token_key = db.StringProperty(required=False)
    access_token_secret = db.StringProperty(required=False)
    verifier = db.StringProperty(required=False)
    
    enabled = db.BooleanProperty(default=False)