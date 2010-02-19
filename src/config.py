#!/usr/bin/env python
# encoding: utf-8

try:
    # create a config_apis.py and set all the values from the template embedded below ... 
    #    it (config_apis.py) is gitignore'd so we don't accidently get each other's api keys
    from config_apis import * # pyflakes:ignore
except ImportError:
    raise ValueError, 'api keys not configured!  Please create a config_apis.py in the src/ dir using the template in config.py'

############################
##config_apis.py begin template:
############################
# import os
#
# TWITTER_CONSUMER_KEY = 'setme'
# TWITTER_CONSUMER_SECRET = 'setme'
# 
# if os.environ.get('SERVER_SOFTWARE', '').startswith('Devel'):
#     TWITTER_CALLBACK = 'http://127.0.0.1:8080/oauth/callback'
# else:
#     TWITTER_CALLBACK = '<setme>.appspot.com/oauth/callback'
# 
# BITLY_LOGIN = 'setme'
# BITLY_API_KEY = 'setme'
############################
##config_apis.py template end
############################
