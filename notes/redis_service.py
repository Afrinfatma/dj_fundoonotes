import redis


class GenericRedis:
    def __init__(self):
        self.redis_cache=redis.Redis(**{"host":'127.0.0.1',"port":6379})

    def setter(self,key,value):
        return self.redis_cache.set(key,value)

    def getter(self,key):
        return self.redis_cache.get(key)
