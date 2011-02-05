from google.appengine.ext import webapp

class Request(webapp.RequestHandler):

    def send(self, data):
        return self.response.out.write(data)
