from google.appengine.ext import webapp

class Request(webapp.RequestHandler):

    def head(self, *args, **kwargs):
        self.get(*args, **kwargs)
        self.response.clear()

    def send(self, data):
        return self.response.out.write(data)
