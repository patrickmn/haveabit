import datetime
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import settings
import db
import quote
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
        quotes = db.getQuotes()[:20]
        for x in quotes:
            items.append(PyRSS2Gen.RSSItem(
                title = x.author.name + ' - ' + x.name,
                link = '%s/%s/%s' % (settings.address, x.author.slug, x.key().id()),
                description = quote.renderTeaser(x) + quote.renderQuote(x, with_title=False),
                # description = linebreaks('%s%s' % (extra, '(' + x.description + '.) ' + '\r\n' + text if x.description else text)),
                guid = PyRSS2Gen.Guid('%s/%s/%s' % (settings.address, x.author.slug, x.key().id())),
                pubDate = x.date))
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
