#!/usr/bin/env python
import operator
from xml.sax.saxutils import quoteattr, escape
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import settings
import db
from request import Request

class MainPage(Request):

    def get(self):
        self.verifyUrl()
        self.response.headers['Cache-Control'] = settings.cache_control
        cached = getCachedPage('index')
        if cached:
            self.send(cached)
        else:
            authors = db.getAuthors()
            split = len(authors) / 2
            list1, list2 = authors[:split], authors[split:]
            template_values = {
                'author_list1': list1,
                'author_list2': list2,
            }
            self.send(getPage('index', 'view/index.html', template_values))

class QuotePage(Request):

    def get(self, author_slug=None, id=None):
        self.verifyUrl()
        author = None
        show_comments = False
        if id:
            try:
                id = int(id)
            except ValueError:
                self.error(404)
                self.send(getNotFoundPage())
                return
            show_comments = bool(self.request.get('show_comments'))
            cached = getCachedPage('quote|%d%s' % (id, '|show_comments' if show_comments else ''))
            if cached:
                self.response.headers['Cache-Control'] = settings.long_cache_control
                self.send(cached)
                return
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
        proper_url = quote.getLink()
        if not self.request.url.startswith(proper_url):
            self.redirect(proper_url, permanent=True)
        else:
            self.response.headers['Cache-Control'] = settings.long_cache_control
            next_quote = db.getNextQuote(quote)
            template_values = {
                'author': author,
                'teaser': quote.renderTeaser(),
                'quote': quote.renderQuote(),
                'quote_name': quote.name,
                'quote_key': quote.key(),
                'quote_url': proper_url,
                'next_quote': next_quote,
                'next_quote_id': next_quote.key().id() if next_quote else None,
                'meta_description': quote.text[:160].replace('\n', '; '),
                'meta_keywords': ', '.join((quote.name, author.name, author.slug)),
                'show_comments': show_comments,
            }
            self.send(getPage('quote|%d%s' % (quote.key().id(), '|show_comments' if show_comments else ''), 'view/quote.html', template_values))

class ListPage(Request):

    def get(self):
        self.verifyUrl()
        self.response.headers['Cache-Control'] = settings.cache_control
        cached = getCachedPage('list')
        if cached:
            self.send(cached)
        else:
            quotes = db.getQuotes()
            quotes.sort(key=operator.attrgetter('date'), reverse=True)
            dates = [x.date.strftime('%Y-%m-%d') for x in quotes]
            ids = [x.key().id() for x in quotes]
            items = zip(quotes, dates, ids)
            template_values = {
                'items': items,
            }
            self.send(getPage('list', 'view/list.html', template_values))

class AboutPage(Request):

    def get(self):
        self.verifyUrl()
        self.response.headers['Cache-Control'] = settings.cache_control
        self.send(getPage('about', 'view/about.html'))

class Api(Request):

    def get(self):
        self.verifyUrl()
        self.response.headers['Cache-Control'] = settings.cache_control
        self.send('api')

class ApiHelp(Request):

    def get(self):
        self.verifyUrl()
        self.response.headers['Cache-Control'] = settings.cache_control
        self.send(getPage('apihelp', 'view/apihelp.html'))

def getNotFoundPage():
    return getPage('404', 'view/404.html')

def getCachedPage(name):
    return memcache.get('page|' + name)

def getPage(name, file, dict=dict()):
    mc_key = 'page|' + name
    val = memcache.get(mc_key)
    if val is None:
        val = template.render(file, dict)
        memcache.set(mc_key, val, settings.page_cache_duration)
    return val

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/about', AboutPage),
                                      ('/list', ListPage),
                                      ('/api', Api),
                                      ('/apihelp', ApiHelp),
                                      ('/random', QuotePage),
                                      (r'/(.*)/(.*)', QuotePage),
                                      (r'/(.*)', QuotePage),
                                      ],
                                     debug=False)

if __name__ == '__main__':
    run_wsgi_app(application)
