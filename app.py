#!/usr/bin/env python
from xml.sax.saxutils import quoteattr, escape
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import settings
import db
if settings.use_strftime:
    import gregtime

class Request(webapp.RequestHandler):

    def send(self, data):
        return self.response.out.write(data)

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
            if author.date_birth:
                dob = gregtime.strftime(author.date_birth, settings.strftime_format) if settings.use_strftime else str(author.date_birth.year)
                if author.date_death:
                    dod = gregtime.strftime(author.date_death, settings.strftime_format) if settings.use_strftime else str(author.date_death.year)
                    lifestr = ' (' + dob + '&ndash;' + dod + ')'
                else:
                    in_prop = '' if settings.use_strftime else 'in '
                    lifestr = ' (born ' + in_prop + dob + ')'
            else:
                lifestr = ''
            next_quote = db.getNextQuote(quote)
            template_values = {
                'author': author,
                'lifestr': lifestr,
                'quote': quote,
                'next_quote': next_quote,
                'next_quote_id': next_quote.key().id() if next_quote else None,
                'meta_description': quote.text[:150],
                'meta_keywords': ', '.join((quote.name, author.name, author.slug)),
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

class Sitemap(Request):

    def get(self):
        self.send(db.getSitemap())

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
                                      ('/api', Api),
                                      ('/apihelp', ApiHelp),
                                      ('/random', QuotePage),
                                      ('/sitemap.xml', Sitemap),
                                      (r'/(.*)/(.*)', QuotePage),
                                      (r'/(.*)', QuotePage),
                                      ],
                                     debug=False)

if __name__ == '__main__':
    run_wsgi_app(application)
