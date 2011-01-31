#!/usr/bin/env python
import datetime
from xml.sax.saxutils import quoteattr, escape
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import model

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

def getAuthor(id=None, name=None):
    query = model.Author.gql("WHERE id = :1 AND name = :2", id, name).fetch(1)
    return query[0]

def getQuote(id=None, author=None):
    query = model.Quote.gql("WHERE id = :1 AND author = :2", id, author).fetch(1)
    if not query:
        query = model.Quote.gql("").fetch(1)
    return query[0]

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/about', AboutPage),
                                      ('/api', Api),
                                      ('/apihelp', ApiHelp)],
                                     debug=False)

if __name__ == '__main__':
    run_wsgi_app(application)
