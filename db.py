import os
import datetime
import random
from google.appengine.ext import db
from google.appengine.api import memcache

import settings

class Category(db.Model):
    name = db.StringProperty()
    slug = db.StringProperty()

class Author(db.Model):
    name = db.StringProperty()
    slug = db.StringProperty()
    description = db.StringProperty()
    img_url = db.StringProperty()
    date_birth = db.DateProperty()
    date_death = db.DateProperty()

class Quote(db.Model):
    author = db.ReferenceProperty(Author)
    categories = db.ListProperty(db.Key)
    name = db.StringProperty()
    description = db.StringProperty()
    text = db.TextProperty()
    img_url = db.StringProperty()
    html = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    rand = db.FloatProperty()

def flush_after(fn):
    def go(*args, **kw):
        ret = fn(*args, **kw)
        flush()
        return ret
    return go

def flush():
    return memcache.flush_all()

def getCategory(slug):
    return Category.gql('WHERE slug = :1', slug).get()

def getAuthor(slug):
    return Author.gql('WHERE slug = :1', slug).get()

def getQuoteByID(id):
    return Quote.get_by_id(id)

def getNextQuote(quote):
    mc_key = 'nextquote|%s' % quote.key().id()
    val = memcache.get(mc_key)
    if val is None:
        res = Quote.gql('WHERE date > :1', quote.date).get()
        if not res:
            query = Quote.gql('WHERE author = :1', quote.author)
            query.order('date')
            res = query.get()
        val = res
        memcache.set(mc_key, val, settings.page_cache_duration)
    return val

def getRandomQuote(author=None):
    # rand = random.random()
    # if author:
    #     res = Quote.gql('WHERE author = :1 AND rand > :2 ORDER BY rand', author, rand).get()
    # else:
    #     res = Quote.gql('WHERE rand > :1 ORDER BY rand', rand).get()
    # val = res
    quotes = getQuotes(author)
    val = quotes[random.randint(0, len(quotes) - 1)]
    return val

def getCategories():
    mc_key = 'categorylist'
    val = memcache.get(mc_key)
    if val is None:
        categories = Category.all()
        categories.order('name')
        val = list(categories)
        memcache.set(mc_key, val, settings.quotelist_cache_duration)
    return val

def getAuthors():
    mc_key = 'authorlist'
    val = memcache.get(mc_key)
    if val is None:
        authors = Author.all()
        authors.order('name')
        val = list(authors)
        memcache.set(mc_key, val, settings.quotelist_cache_duration)
    return val

def getQuotes(author=None):
    if author:
        mc_key = 'quotelist|' + author.name
    else:
        mc_key = 'quotelist'
    val = memcache.get(mc_key)
    if val is None:
        val = []
        if author:
            query = Quote.gql('WHERE author = :1', author)
        else:
            query = Quote.all()
        for x in query:
            val.append(x)
        memcache.set(mc_key, val, settings.quotelist_cache_duration)
    return val

def getSitemap():
    mc_key = 'sitemap'
    val = memcache.get(mc_key)
    if val is None:
        host = os.environ['HTTP_HOST'] if os.environ.get('HTTP_HOST') else os.environ['SERVER_NAME']
        sitemap = []
        sitemap.append('<?xml version="1.0" encoding="UTF-8"?>')
        sitemap.append('<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        quotes = getQuotes()
        for quote in quotes:
            entry = '<url><loc>%s/%s/%s</loc></url>' % (host, quote.author.slug, quote.key().id())
            sitemap.append(entry)
        sitemap.append('</urlset>')
        val = u'\r\n'.join(sitemap)
        memcache.set(mc_key, val, settings.page_cache_duration)
    return val

@flush_after
def addCategory(name, slug):
    res = Category.gql('WHERE slug = :1', slug).get()
    if res:
        category = res
    else:
        category = Category()
    category.name = name
    category.slug = slug
    category.put()

@flush_after
def addAuthor(name, slug, description, img_url, date_birth, date_death):
    res = Author.gql('WHERE slug = :1', slug).get()
    if res:
        author = res
        # Slug is not changed for existing authors as it's part of the URL
    else:
        author = Author()
        author.slug = slug
    if name:
        author.name = name
    author.description = description
    author.img_url = img_url
    if date_birth:
        author.date_birth = datetime.date(*[int(x) for x in date_birth.split('-')])
    if date_death:
        author.date_death = datetime.date(*[int(x) for x in date_death.split('-')])
    author.put()

@flush_after
def addQuote(author, cats, name, description, text, img_url, html):
    categories = []
    quote = Quote()
    quote.author = author
    quote.categories = [getCategory(x).key() for x in cats]
    quote.name = name
    quote.description = description
    quote.text = text
    quote.img_url = img_url
    quote.html = html
    has = Quote.gql('WHERE author = :1', author).get()
    quote.rand = 1.0 if not has else random.random()
    quote.put()
