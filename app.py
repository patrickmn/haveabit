#!/usr/bin/env python
import datetime
from xml.sax.saxutils import quoteattr, escape
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import db

class Request(webapp.RequestHandler):

    def send(self, data):
        return self.response.out.write(data)

class MainPage(Request):

    def get(self):
        self.send(template.render('view/index.html', dict()))

class AboutPage(Request):

    def get(self):
        self.send(template.render('view/about.html', dict()))

class Api(Request):

    def get(self):
        self.send('api')

class ApiHelp(Request):

    def get(self):
        self.send(template.render('view/apihelp.html', dict()))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/about', AboutPage),
                                      ('/api', Api),
                                      ('/apihelp', ApiHelp)],
                                     debug=False)

if __name__ == '__main__':
    run_wsgi_app(application)
