import redis

HOST = "127.0.0.1"
PORT = 6379


class _RedisClient:
    client = redis.Redis


