import os

use_strftime = False
strftime_format = '%b %e, %Y'
long_cache_control = 'public, max-age=86400' # Default browser Cache-Control for pages that rarely change
cache_control = 'public, max-age=3600'       # Default browser Cache-Control for pages that might change
page_cache_duration = 2591999                # How many seconds to cache (static) rendered pages (max: 2591999)
quotelist_cache_duration = 2591999           # How many seconds to cache lists of quotes (max: 2591999)
# quotelist_cache_duration = 3600

address = 'http://' + os.environ['HTTP_HOST'] if os.environ.get('HTTP_HOST') else os.environ['SERVER_NAME']
