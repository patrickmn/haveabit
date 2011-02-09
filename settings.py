import os

use_strftime = False
strftime_format = '%b %e, %Y'
cache_control = 'public, max-age=3600'       # Default browser Cache-Control for pages that might change
long_cache_control = 'public, max-age=7200'  # Default browser Cache-Control for pages that rarely change
page_cache_duration = 2591999                # How many seconds to cache (static) rendered pages (max: 2591999)
quotelist_cache_duration = 2591999           # How many seconds to cache lists of quotes (max: 2591999)
# quotelist_cache_duration = 3600

if os.environ.get('SERVER_SOFTWARE').startswith('Development'):
    hostname = os.environ['HTTP_HOST'] if os.environ.get('HTTP_HOST') else os.environ['SERVER_NAME']
else:
    hostname = 'www.haveabit.com'
address = 'http://' + hostname
