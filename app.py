#!/usr/bin/env python
from xml.sax.saxutils import quoteattr, escape
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import config
import db

class Request(webapp.RequestHandler):

    def send(self, data):
        return self.response.out.write(data)

class MainPage(Request):

    def get(self):
        template_values = {
            'authors': db.getAuthors(),
        }
        self.send(getPage('index', 'view/index.html', template_values))

class QuotePage(Request):

    def get(self, author_slug=None, id=None):
        author = None
        if id:
            id = int(id)
            quote = db.getQuoteByID(id)
            if quote:
                author = quote.author
            else:
                self.error(404)
                self.send(getNotFoundPage())
                return
        elif author_slug:
            author = db.getAuthor(author_slug)
            if author:
                quote = db.getRandomQuote(author)
            else:
                self.error(404)
                self.send(getNotFoundPage())
                return
        else:
            quote = db.getRandomQuote()
            author = quote.author
        proper_url = '/%s/%d' % (author.slug, quote.key().id())
        if not self.request.path == proper_url:
            self.redirect(proper_url)
        else:
            template_values = {
                'author': author,
                'quote': quote,
            }
            self.send(getPage('quote|%d' % quote.key().id(), 'view/quote.html', template_values))

class AboutPage(Request):

    def get(self):
        self.send(getPage('about', 'view/about.html'))

class Api(Request):

    def get(self):
        self.send('api')

class ApiHelp(Request):

    def get(self):
        self.send(getPage('apihelp', 'view/apihelp.html'))

def getNotFoundPage():
    return getPage('404', 'view/404.html')

def getPage(name, file, dict=dict()):
    mc_key = 'page|' + name
    val = memcache.get(mc_key)
    if val is None:
        val = template.render(file, dict)
        memcache.set(mc_key, val, config.page_cache_duration)
    return val

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/about', AboutPage),
                                      ('/api', Api),
                                      ('/apihelp', ApiHelp),
                                      ('/random', QuotePage),
                                      (r'/(.*)/(.*)', QuotePage),
                                      (r'/(.*)', QuotePage),
                                      ],
                                     debug=False)

if __name__ == '__main__':
    run_wsgi_app(application)
