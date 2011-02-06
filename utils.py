import urllib2
from google.appengine.api.images import Image

def downloadFile(url):
    data = urllib2.urlopen(url).read()
    return data

def getImageDimensions(file):
    img = Image(file)
    return img.width, img.height

def refreshImageDimensions(obj):
    # obj can be either Author or Quote
    if obj.img_url:
        obj.img_width, obj.img_height = getImageDimensions(downloadFile(obj.img_url))
        obj.put()
        return True
