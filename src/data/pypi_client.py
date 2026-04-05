from concurrent.futures import ThreadPoolExecutor
from loguru import logger
from requests.exceptions import RequestException
import requests
import time

def get_lib(lib: str) -> dict | None:
    """Fetch download statistics for a single package from PyPI Stats.

    Waits 0.3 seconds before each request to avoid overwhelming the PyPI
    Stats API when called concurrently.

    Parameters
    ----------
    lib : str
        PyPI package name (e.g. ``"numpy"``).

    Returns
    -------
    dict or None
        PyPI Stats API response as a dictionary, or ``None`` if the request fails.

    Examples
    --------
    >>> stats = get_lib("numpy")
    >>> stats["data"][0]["downloads"]
    12345678
    """

    time.sleep(0.3)
    
    try:
        url = f"https://pypistats.org/api/packages/{lib.lower()}/overall"
        
        response = requests.get(url, timeout=15)
        
        response.raise_for_status()
        
        stats_json = response.json()
        
        return stats_json
        
    except RequestException as e:
        logger.error(e)
        return None
    
def get_libs(libs: list) -> list[dict | None]:
    """Fetch download statistics for multiple packages concurrently.

    Uses a thread pool of 3 workers. Each worker sleeps 0.3 seconds before
    requesting, spacing out calls to the PyPI Stats API. Results preserve
    the order of the input list.

    Parameters
    ----------
    libs : list
        PyPI package names to fetch.

    Returns
    -------
    list of dict or None
        One entry per input package; ``None`` for any that failed.
    """
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(get_lib, libs)
            
    return list(results)