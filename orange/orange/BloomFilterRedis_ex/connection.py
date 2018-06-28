import redis

# default bloom filter redis config
BLOOM_REDIS_URL = None
BLOOM_REDIS_HOST = 'localhost'
BLOOM_REDIS_PORT = 6379
BLOOM_REDIS_DB = 9


def bloom_filter_from_settings(settings):
    url = settings.get('BLOOM_REDIS_URL', BLOOM_REDIS_URL)
    host = settings.get('BLOOM_REDIS_HOST', BLOOM_REDIS_HOST)
    port = settings.get('BLOOM_REDIS_PORT', BLOOM_REDIS_PORT)
    db = settings.get('BLOOM_REDIS_DB', BLOOM_REDIS_DB)

    _redis = redis.StrictRedis

    return _redis.from_url(BLOOM_REDIS_URL) if url else \
        _redis(host=host, port=port, db=db)
