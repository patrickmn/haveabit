from google.appengine.ext import db

class Category(db.Model):
    name = db.StringProperty()
    slug = db.StringProperty()

class Author(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()

class Quote(db.Model):
    author = db.ReferenceProperty(Author)
    category = db.ReferenceProperty(Category)
    text = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
