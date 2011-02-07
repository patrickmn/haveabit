import datetime
import random
from google.appengine.ext import db
from google.appengine.api import memcache

import settings
import bit

class Category(db.Model):
    name = db.StringProperty()
    slug = db.StringProperty()

class Author(db.Model):
    name = db.StringProperty()
    slug = db.StringProperty()
    description = db.StringProperty()
    img_url = db.StringProperty()
    img_width = db.IntegerProperty()
    img_height = db.IntegerProperty()
    date_birth = db.DateProperty()
    date_death = db.DateProperty()

class Quote(db.Model, bit.Quote):
    author = db.ReferenceProperty(Author)
    categories = db.ListProperty(db.Key)
    name = db.StringProperty()
    description = db.StringProperty()
    text = db.TextProperty()
    img_url = db.StringProperty()
    img_width = db.IntegerProperty()
    img_height = db.IntegerProperty()
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
        val = Quote.gql('WHERE author = :1 AND date > :2 ORDER BY date', quote.author, quote.date).get()
        if not val:
            val = Quote.gql('WHERE author = :1 ORDER BY date', quote.author).get()
        memcache.set(mc_key, val, settings.page_cache_duration)
    if not val.key() == quote.key():
        return val

def getRandomQuote(author=None):
    # rand = random.random()
    # if author:
    #     res = Quote.gql('WHERE author = :1 AND rand > :2 ORDER BY rand', author, rand).get()
    # else:
    #     res = Quote.gql('WHERE rand > :1 ORDER BY rand', rand).get()
    # val = res
    ids = getQuoteIDs(author)
    id = ids[random.randint(0, len(ids) - 1)]
    return getQuoteByID(id)

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
        mc_key = 'quotelist|%s' % author.name
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

def getQuoteIDs(author=None):
    if author:
        mc_key = 'quoteidlist|%s' % author.name
    else:
        mc_key = 'quoteidlist'
    val = memcache.get(mc_key)
    if val is None:
        if author:
            query = Quote.gql('WHERE author = :1', author)
        else:
            query = Quote.all()
        val = [x.key().id() for x in query]
        memcache.set(mc_key, val, settings.quotelist_cache_duration)
    return val

def getRecentQuotes(number=20):
    mc_key = 'recentquotelist|%s' % number
    val = memcache.get(mc_key)
    if val is None:
        query = Quote.all()
        query.order('-date')
        val = query.fetch(number)
        memcache.set(mc_key, val, settings.quotelist_cache_duration)
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
def addAuthor(name, slug, description, date_birth, date_death, img_url, img_width=None, img_height=None):
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
    author.img_width = img_width
    author.img_height = img_height
    if date_birth:
        author.date_birth = datetime.date(*[int(x) for x in date_birth.split('-')])
    if date_death:
        author.date_death = datetime.date(*[int(x) for x in date_death.split('-')])
    author.put()

@flush_after
def addQuote(author, categories, name, description, text, html, img_url, img_width=None, img_height=None, quote_id=None):
    if quote_id:
        quote = getQuoteByID(int(quote_id))
    else:
        quote = Quote()
    quote.author = author
    quote.categories = [getCategory(x).key() for x in categories]
    quote.name = name
    quote.description = description
    quote.text = text
    quote.img_url = img_url
    quote.img_width = img_width
    quote.img_height = img_height
    quote.html = html
    has = Quote.gql('WHERE author = :1', author).get()
    quote.rand = 1.0 if not has else random.random()
    quote.put()
