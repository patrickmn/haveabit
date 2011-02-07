from google.appengine.ext import webapp

import settings

class Request(webapp.RequestHandler):

    def head(self, *args, **kwargs):
        self.get(*args, **kwargs)
        self.response.clear()

    def send(self, data):
        return self.response.out.write(data)

    def verifyUrl(self):
        if not self.request.url.startswith(settings.address):
            self.redirect(settings.address + self.request.path, permanent=True)
            return
