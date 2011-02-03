import os

page_cache_duration = 2592000   # How many seconds to cache (static) rendered pages
quotelist_cache_duration = 3600 # How many seconds to cache lists of quotes
mc_base = os.environ['CURRENT_VERSION_ID'] + '|'
