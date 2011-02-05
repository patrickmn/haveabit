import datetime
import operator
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import settings
import db
import PyRSS2Gen
from request import Request

class Feed(Request):

    def get(self):
        if self.request.headers['User-Agent'].startswith('FeedBurner'):
            self.send(getFeed())
        else:
            self.redirect('http://feeds.haveabit.com/haveabit', permanent=True)

def getFeed():
    mc_key = 'feed'
    val = memcache.get(mc_key)
    if val is None:
        items = []
        quotes = db.getRecentQuotes(20)
        for quote in quotes:
            link = quote.getLink()
            items.append(PyRSS2Gen.RSSItem(
                title = quote.author.name + ' - ' + quote.name,
                link = quote.getLink(),
                description = quote.renderTeaser() + quote.renderQuote(with_title=False),
                guid = PyRSS2Gen.Guid(link),
                pubDate = quote.date))
        rss = PyRSS2Gen.RSS2(
            title = 'Have a Bit',
            link = settings.address,
            description = 'The latest bits from Have a Bit -- your inspirational quote source.',
            lastBuildDate = datetime.datetime.utcnow(),
            items = items)
        val = rss.to_xml()
        memcache.set(mc_key, val, settings.page_cache_duration)
    return val

application = webapp.WSGIApplication(
                                     [('/feed', Feed),
                                      ],
                                     debug=False)

if __name__ == '__main__':
    run_wsgi_app(application)
