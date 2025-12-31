import json
from .redis_client import redis_client

def cache_set(key, value, ttl=60):
    redis_client.setex(key, ttl, json.dumps(value))

def cache_get(key):
    raw = redis_client.get(key)
    if not raw:
        return None
    return json.loads(raw)
