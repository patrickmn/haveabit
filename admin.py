#!/usr/bin/env python
import datetime
from xml.sax.saxutils import quoteattr, escape
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import db

class Request(webapp.RequestHandler):

    def send(self, data):
        return self.response.out.write(data)

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
            name = self.request.get('name')
            slug = self.request.get('slug')
            description = self.request.get('description')
            img_url = self.request.get('img_url')
            date_birth = self.request.get('date_birth')
            date_death = self.request.get('date_death')
            if db.addAuthor(name, slug, description, img_url, date_birth, date_death):
                res = 1
            self.redirect('/admin?res=%d' % res)
        elif type == 'quote':
            author = db.getAuthor(self.request.get('author'))
            categories = self.request.get_all('category')
            name = self.request.get('name')
            text = self.request.get('text')
            img_url = self.request.get('img_url')
            vid_url = self.request.get('vid_url')
            if db.addQuote(author, categories, name, text, img_url, vid_url):
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
