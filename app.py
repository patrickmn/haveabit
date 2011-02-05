#!/usr/bin/env python
import operator
from xml.sax.saxutils import quoteattr, escape
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import settings
import db
if settings.use_strftime:
    import gregtime
import quote
from request import Request

class MainPage(Request):

    def get(self):
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
        author = None
        if id:
            id = int(id)
            q = db.getQuoteByID(id)
            if q:
                author = q.author
            else:
                self.error(404)
                self.send(getNotFoundPage())
                return
        elif author_slug:
            author = db.getAuthor(author_slug)
            if author:
                q = db.getRandomQuote(author)
            else:
                self.error(404)
                self.send(getNotFoundPage())
                return
        else:
            q = db.getRandomQuote()
            author = q.author
        proper_url = '/%s/%d' % (author.slug, q.key().id())
        if not self.request.path == proper_url:
            self.redirect(proper_url)
        else:
            next_quote = db.getNextQuote(q)
            template_values = {
                'author': author,
                'teaser': quote.renderTeaser(q),
                'quote': quote.renderQuote(q),
                'quote_name': q.name,
                'next_quote': next_quote,
                'next_quote_id': next_quote.key().id() if next_quote else None,
                'meta_description': q.text[:160],
                'meta_keywords': ', '.join((q.name, author.name, author.slug)),
            }
            self.send(getPage('quote|%d' % q.key().id(), 'view/quote.html', template_values))

class ListPage(Request):

    def get(self):
        quotes = db.getQuotes()
        dates = [x.date.strftime('%Y-%m-%d') for x in quotes]
        ids = [x.key().id() for x in quotes]
        items = zip(quotes, dates, ids)
        items = sorted(items, key=operator.itemgetter(1), reverse=True)
        template_values = {
            'items': items,
        }
        self.send(getPage('list', 'view/list.html', template_values))

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
