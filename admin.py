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
        self.send(template.render('view/admin/index.html', dict()))

class Add(Request):

    def get(self):
        self.send("Add!")

class Bootstrap(Request):

    def get(self):
        category = db.Category()
        author = db.Author()
        quote = db.Quote()
        category.name = 'Classic'
        category.slug = 'classic'
        category.put()
        author.name = 'Rene Descartes'
        author.slug = 'descartes'
        author.description = 'Rene Descartes was a natural philosopher, and writer who spent most of his adult life in the Dutch Republic. He has been dubbed the "Father of Modern Philosophy", and much subsequent Western philosophy is a response to his writings, which are studied closely to this day.'
        author.put()
        quote.text = 'Cogito ergo sum.'
        quote.author = author
        quote.categories.append(category.key())
        quote.put()
        self.send("Added Descartes quote.")

application = webapp.WSGIApplication(
                                     [('/admin', MainPage),
                                      (r'/admin/add/(.*)/(.*)', Add),
                                      ('/admin/bootstrap', Bootstrap),
                                      ],
                                     debug=True)

if __name__ == '__main__':
    run_wsgi_app(application)
