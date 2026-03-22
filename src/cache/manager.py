from diskcache import Cache
from pathlib import Path
from typing import Callable

def start_cache():

    cache_path = Path(__file__).parent.parent.parent/".temp"/"cache"

    cache = Cache(cache_path)
    
    return cache

def get_or_set_value_from_cache(key: str, func: Callable):
    
    cache = start_cache()
    
    has_key = cache.get(key)    
    if has_key:
        return has_key
    else:
        value = func()
        cache.set(key=key, value=value, expire=24*3600)
        return value