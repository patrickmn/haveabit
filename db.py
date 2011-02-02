import random
from google.appengine.ext import db

class Category(db.Model):
    name = db.StringProperty()
    slug = db.StringProperty()

class Author(db.Model):
    name = db.StringProperty()
    slug = db.StringProperty()
    description = db.TextProperty()
    img_url = db.StringProperty()

class Quote(db.Model):
    author = db.ReferenceProperty(Author)
    categories = db.ListProperty(db.Key)
    name = db.StringProperty()
    text = db.TextProperty()
    img_url = db.StringProperty()
    vid_url = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    rand = db.FloatProperty()

def getCategory(slug):
    query = Category.gql('WHERE slug = :1', slug).fetch(1)
    if query:
        return query[0]

def getAuthor(slug):
    query = Author.gql('WHERE slug = :1', slug).fetch(1)
    if query:
        return query[0]

def getQuoteByID(id):
    return Quote.get_by_id(id)

def getRandomQuote(author=None):
    rand = random.random()
    if author:
        query = Quote.gql('WHERE author = :1 AND rand > :2 ORDER BY rand', author, rand).fetch(1)
    else:
        query = Quote.gql('WHERE rand > :1 ORDER BY rand', rand).fetch(1)
    val = query[0]
    return val

def getCategories():
    result = []
    query = Category.all()
    for x in query:
        result.append((x.slug, x.name))
    return result

def getAuthors():
    result = []
    query = Author.all()
    for x in query:
        result.append((x.slug, x.name, x.description))
    return result

def addCategory(name, slug):
    query = Category.gql('WHERE slug = :1', slug).fetch(1)
    if query:
        category = query[0]
    else:
        category = Category()
    category.name = name
    category.slug = slug
    category.put()

def addAuthor(name, slug, description, img_url):
    query = Author.gql('WHERE slug = :1', slug).fetch(1)
    if query:
        author = query[0]
    else:
        author = Author()
    author.name = name
    author.slug = slug
    author.description = description
    author.img_url = img_url
    author.put()

def addQuote(author, cats, name, text, img_url, vid_url):
    categories = []
    quote = Quote()
    quote.author = author
    quote.categories = [getCategory(x).key() for x in cats]
    quote.name = name
    quote.text = text
    quote.img_url = img_url
    quote.vid_url = vid_url
    has = Quote.gql('WHERE author = :1', author).fetch(1)
    quote.rand = 1.0 if not has else random.random()
    quote.put()
