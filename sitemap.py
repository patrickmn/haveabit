import os
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import db
import settings
from request import Request

class Sitemap(Request):

    def get(self):
        self.send(getSitemap())

def getSitemap():
    mc_key = 'sitemap'
    val = memcache.get(mc_key)
    if val is None:
        sitemap = []
        sitemap.append('<?xml version="1.0" encoding="UTF-8"?>')
        sitemap.append('<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        quotes = db.getQuotes()
        for quote in quotes:
            entry = '<url><loc>%s</loc></url>' % (quote.getUrl())
            sitemap.append(entry)
        sitemap.append('</urlset>')
        val = u'\r\n'.join(sitemap)
        memcache.set(mc_key, val, settings.page_cache_duration)
    return val

application = webapp.WSGIApplication(
                                     [('/sitemap.xml', Sitemap),
                                      ],
                                     debug=False)

if __name__ == '__main__':
    run_wsgi_app(application)
