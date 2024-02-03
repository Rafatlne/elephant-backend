import redis
from django.conf import settings

# Global Redis connection pool
redis_pool = None


def get_redis_pool():
    global redis_pool
    if not redis_pool:
        redis_url = settings.MAIN_REDIS_URL

        redis_pool = redis.ConnectionPool.from_url(redis_url)

    return redis_pool
