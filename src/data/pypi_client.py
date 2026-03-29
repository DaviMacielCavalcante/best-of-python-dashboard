from concurrent.futures import ThreadPoolExecutor
from loguru import logger
from requests.exceptions import RequestException
import requests
import time

def get_lib(lib: str) -> dict | None:
    
    try:
        url = f"https://pypistats.org/api/packages/{lib.lower()}/overall"
        
        response = requests.get(url)
        
        response.raise_for_status()
        
        stats_json = response.json()
        
        return stats_json
        
    except RequestException as e:
        logger.error(e)
        return None
    
def get_libs(libs: list) -> list[dict | None]:
    time.sleep(0.3)
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(get_lib, libs)
            
    return list(results)