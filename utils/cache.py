import memcache

cache = memcache.Client(['127.0.0.1:11211'],debug=True)  #确认memcache 是不是启动git

def set(key,value,timeout=60):
    return cache.set(key,value,timeout)
def get(key):
    return cache.get(key)
def delete(key):
    return cache.delete(key)

