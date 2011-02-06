import os

use_strftime = False
strftime_format = '%b %e, %Y'
cache_control = 'public, max-age=3600' # Default browser Cache-Control for static pages
page_cache_duration = 2591999          # How many seconds to cache (static) rendered pages (max: 2591999)
quotelist_cache_duration = 2591999     # How many seconds to cache lists of quotes (max: 2591999)
# quotelist_cache_duration = 3600

address = 'http://' + os.environ['HTTP_HOST'] if os.environ.get('HTTP_HOST') else os.environ['SERVER_NAME']
