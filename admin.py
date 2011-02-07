#!/usr/bin/env python
from xml.sax.saxutils import quoteattr, escape
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import db
import utils
from request import Request

class MainPage(Request):

    def get(self):
        authors = db.getAuthors()
        categories = db.getCategories()
        template_values = {
            'authors': authors,
            'categories': categories,
        }
        self.send(template.render('view/admin/index.html', template_values))

class Add(Request):

    def post(self, type):
        res = 0
        if type == 'category':
            name = self.request.get('name')
            slug = self.request.get('slug')
            if db.addCategory(name, slug):
                res = 1
            self.redirect('/admin?res=%d' % res)
        elif type == 'author':
            img_url = self.request.get('img_url')
            if img_url:
                img_width, img_height = utils.getImageDimensions(utils.downloadFile(img_url))
            else:
                img_width = None
                img_height = None
            if db.addAuthor(name = self.request.get('name'),
                            slug = self.request.get('slug'),
                            description = self.request.get('description'),
                            date_birth = self.request.get('date_birth'),
                            date_death = self.request.get('date_death'),
                            img_url = img_url,
                            img_width = img_width,
                            img_height = img_height):
                res = 1
            self.redirect('/admin?res=%d' % res)
        elif type == 'quote':
            img_url = self.request.get('img_url')
            if img_url:
                img_width, img_height = utils.getImageDimensions(utils.downloadFile(img_url))
            else:
                img_width = None
                img_height = None
            if db.addQuote(quote_id = self.request.get('quote_id'),
                           author = db.getAuthor(self.request.get('author')),
                           categories = self.request.get_all('category'),
                           name = self.request.get('name'),
                           description = self.request.get('description'),
                           text = self.request.get('text'),
                           html = self.request.get('html'),
                           img_url = img_url,
                           img_width = img_width,
                           img_height = img_height):
                res = 1
            self.redirect('/admin?res=%d' % res)

class Flush(Request):

    def post(self):
        res = 0
        if memcache.flush_all():
            res = 1
        self.redirect('/admin?res=%d' % res)

application = webapp.WSGIApplication(
                                     [('/admin', MainPage),
                                      ('/admin/flush', Flush),
                                      (r'/admin/add/(.*)', Add),
                                      ],
                                     debug=True)

if __name__ == '__main__':
    run_wsgi_app(application)
