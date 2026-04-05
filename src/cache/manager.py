from diskcache import Cache
from pathlib import Path
from typing import Callable
from datetime import datetime

cache_path = Path(__file__).parent.parent.parent/".temp"/"cache"

cache = Cache(cache_path)

def get_or_set_value_from_cache(key: str, func: Callable):
    """Return a cached value, or compute and cache it if not present.

    On cache miss, calls ``func()``, stores the result with a 24-hour TTL,
    and records the current date under ``{key}_last_update``.

    Parameters
    ----------
    key : str
        Cache key.
    func : Callable
        Zero-argument callable used to compute the value on a cache miss.

    Returns
    -------
    Any
        The cached or freshly computed value.
    """
    
    _MISSING = object() 
    
    has_key = cache.get(key, default=_MISSING)   
    
    if has_key is not _MISSING:
        return has_key
    else:
        value = func()
        cache.set(key=key, value=value, expire=24*3600)
        cache.set(key=f"{key}_last_update", value=datetime.now().strftime("%Y-%m-%d"))
        return value
    
def get_last_update(key: str):
    """Return the date the cache entry was last populated.

    Parameters
    ----------
    key : str
        Base cache key (without the ``_last_update`` suffix).

    Returns
    -------
    str or None
        Date string in ``YYYY-MM-DD`` format, or ``None`` if never cached.
    """
        
    return cache.get(f"{key}_last_update")