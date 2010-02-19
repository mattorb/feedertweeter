#!/usr/bin/python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from src.utils import pathfix # pyflakes:ignore

import views
import tasks.poller

application = webapp.WSGIApplication([
                                     (r'/oauth/callback', views.OAuthCallbackPage),
                                     (r'/create', views.CreatePage),
                                     (r'/tasks/poller', tasks.poller.Poller)
                                     ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
