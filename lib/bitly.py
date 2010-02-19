import cgi
 
from django.utils import simplejson
from google.appengine.api import urlfetch
 
class BitLy():
	def __init__(self, login, apikey):
		self.login = login
		self.apikey = apikey
 
	def expand(self,param):
		request = "http://api.bit.ly/expand?version=2.0.1&shortUrl=http://bit.ly/"
		request += param
		request += "&login=" + self.login + "&apiKey=" +self.apikey
 
		result = urlfetch.fetch(request)
		json = simplejson.loads(result.content)
		return json
 
	def shorten(self,param):
		url = "http://" + param
		request = "http://api.bit.ly/shorten?version=2.0.1&longUrl="
		request += url
		request += "&login=" + self.login + "&apiKey=" +self.apikey
 
		result = urlfetch.fetch(request)
		json = simplejson.loads(result.content)
		return json
 
	def info(self,param):
		request = "http://api.bit.ly/info?version=2.0.1&hash="
		request += param
		request += "&login=" + self.login + "&apiKey=" +self.apikey
 
		result = urlfetch.fetch(request)
		json = simplejson.loads(result.content)
		return json
 
	def stats(self,param):
		request = "http://api.bit.ly/stats?version=2.0.1&shortUrl="
		request += param
		request += "&login=" + self.login + "&apiKey=" +self.apikey
 
		result = urlfetch.fetch(request)
		json = simplejson.loads(result.content)
		return json
 
	def errors(self):
		request = "http://api.bit.ly/errors?version=2.0.1&login=" + self.login + "&apiKey=" +self.apikey
 
		result = urlfetch.fetch(request)
		json = simplejson.loads(result.content)
		return json
