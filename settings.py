import os

use_strftime = False
strftime_format = '%b %e, %Y'
page_cache_duration = 2592000   # How many seconds to cache (static) rendered pages
quotelist_cache_duration = 3600 # How many seconds to cache lists of quotes

address = 'http://' + os.environ['HTTP_HOST'] if os.environ.get('HTTP_HOST') else os.environ['SERVER_NAME']
