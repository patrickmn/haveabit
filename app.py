#!/usr/bin/env python
from xml.sax.saxutils import quoteattr, escape
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import db

page_cache_duration = 2592000 # How many seconds to cache (static) rendered pages

class Request(webapp.RequestHandler):

    def send(self, data):
        return self.response.out.write(data)

class MainPage(Request):

    def get(self):
        self.send(getStaticPage('index', 'view/index.html'))

class AboutPage(Request):

    def get(self):
        self.send(getStaticPage('about', 'view/about.html'))

class Api(Request):

    def get(self):
        self.send('api')

class ApiHelp(Request):

    def get(self):
        self.send(getStaticPage('apihelp', 'view/apihelp.html'))

def getStaticPage(name, file):
    memcachekey = 'page|' + name
    val = memcache.get(memcachekey)
    if val is None:
        val = template.render(file, dict())
        memcache.set(memcachekey, val, page_cache_duration)
    return val

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/about', AboutPage),
                                      ('/api', Api),
                                      ('/apihelp', ApiHelp)],
                                     debug=False)

if __name__ == '__main__':
    run_wsgi_app(application)
