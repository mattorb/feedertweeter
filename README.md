#FeederTweeter 
## What is it?
App engine/py experiment to tweet new entries from an atom feed to a twitter account.  It shortens urls w/bit.ly.   
It tweets based on a template you specify.

## To Install it (locally)
Clone the repo, then create a config_apis.py file (using the template at the bottom of config.py) and fill in the values for your
twitter and bitly api keys.

## To Install it (to your appengine account)
Do all the local install stuff, then modify the app id in app.yaml.   

## Dev notes 
I'm using Ale to continuously lint and run tests.  Install it with 'git submodule init', then 'git submodule update'.
Set up the test routine with 'ale install test', 'ale install pyflakes', then 'ale install watcher'.  
To start the continuous test runner use 'ale watcher'

## Libraries used
Universal feed Parser
Tweepy

##To-do
Prioritized:
-

Not prioritized:
- tests around length limiting (for twitter 140 char limit)
- error handling all around
- visual revamp
- smoke/integration tests