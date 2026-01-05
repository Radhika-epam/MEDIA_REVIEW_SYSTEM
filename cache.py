import redis
import json

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_cache(key):
    data = cache.get(key)
    return json.loads(data) if data else None

def set_cache(key, value):
    cache.set(key, json.dumps(value))
