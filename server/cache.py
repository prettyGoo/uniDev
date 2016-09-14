import sys
import socket
import json
import redis

class RedisCache:

    def __init__(self, host='localhost', port=6379, db=0):
        self.cache = redis.StrictRedis(host=host, port=port, db=db)

    def append(self, key, val):
        self.cache.append(key, val)

    def get(self, key):
        return self.cache.get(key)

    def flushall(self):
        self.cache.flushall()

    def dbsize(self):
        return self.cache.dbsize()
