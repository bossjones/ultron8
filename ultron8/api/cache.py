"""Creates a cache instance w/ redis as a backend.

Use `cache` to interact with the cache.

Objects are pickled before getting sent into redis.
"""
from aiocache import caches

from ultron8.api import settings

# RE: caching https://github.com/tiangolo/fastapi/issues/651

# A warning about JSON serialization
# https://tech.zarmory.com/2019/02/a-warning-about-json-serialization.html
############################################################################################
# I added caching capabilities for one of my projects by using aiocache with JSON serializer. While doing that I came over strange issue where I was putting {1: "a"} in cache, but received {"1": "a"} on retrieval - the 1 integer key came back as "1" string. First I thought it's an bug in aiocache, but maintainer kindly pointed out that JSON, being Javascript Object Notation does not allow mapping keys to be non-strings.

# However there is a point here that's worth paying attention to - it looks like JSON libraries, at least in Python and Chrome/Firefox, will happily accept {1: "a"} for encoding but will convert keys to strings. This may lead to quite subtle bugs as in my earlier example - cache hits will return data different to original.
############################################################################################

# if settings.TESTING:
#     config = {
#         'default': {
#             'cache': 'aiocache.SimpleMemoryCache',
#             'serializer': {
#                 'class': 'aiocache.serializers.PickleSerializer'
#             }
#         },
#     }
# else:
#     config = {
#         'default': {
#             'cache': 'aiocache.RedisCache',
#             'endpoint': settings.REDIS_ENDPOINT,
#             'port': settings.REDIS_PORT,
#             'db': settings.REDIS_DB,
#             'serializer': {
#                 'class': 'aiocache.serializers.PickleSerializer'
#             }
#         },
#     }
#     if settings.REDIS_PASSWORD:
#         config['default']['password'] = str(settings.REDIS_PASSWORD)

# DISABLED: # might be causing conflict with json data being returned # config = {
# DISABLED: # might be causing conflict with json data being returned #     "default": {
# DISABLED: # might be causing conflict with json data being returned #         "cache": "aiocache.SimpleMemoryCache",
# DISABLED: # might be causing conflict with json data being returned #         "serializer": {"class": "aiocache.serializers.PickleSerializer"},
# DISABLED: # might be causing conflict with json data being returned #     }
# DISABLED: # might be causing conflict with json data being returned # }
# DISABLED: # might be causing conflict with json data being returned #
# DISABLED: # might be causing conflict with json data being returned # caches.set_config(config)
# DISABLED: # might be causing conflict with json data being returned #
# DISABLED: # might be causing conflict with json data being returned # cache = caches.get("default")
