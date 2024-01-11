import redis


class RedisService:

    def __init__(self):
        self.client = redis.Redis(host='redis', port=6379)

    def set(self, key: str, value: str, ex: int | None = None):
        self.client.set(key, value, nx=True, ex=ex)

    def get(self, key: str):
        return self.client.get(key)
