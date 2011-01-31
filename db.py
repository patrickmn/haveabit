from google.appengine.ext import db

class Category(db.Model):
    name = db.StringProperty()
    slug = db.StringProperty()

class Author(db.Model):
    name = db.StringProperty()
    slug = db.StringProperty()
    description = db.StringProperty()

class Quote(db.Model):
    author = db.ReferenceProperty(Author)
    categories = db.ListProperty(db.Key)
    text = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

def getAuthor(id=None, name=None):
    query = Author.gql("WHERE id = :1 AND name = :2", id, name).fetch(1)
    return query[0]

def getQuote(id=None, author=None):
    query = Quote.gql("WHERE id = :1 AND author = :2", id, author).fetch(1)
    if not query:
        query = Quote.gql("").fetch(1)
    return query[0]
