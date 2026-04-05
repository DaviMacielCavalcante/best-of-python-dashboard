from loguru import logger
from yaml import YAMLError
from requests.exceptions import RequestException
import requests 
import yaml

def load() -> dict | None:
    """Fetch and parse the best-of-python projects list from GitHub.

    Downloads ``projects.yaml`` from the lukasmasuch/best-of-python repository
    and parses it into a Python dictionary.

    Returns
    -------
    dict or None
        Parsed YAML content as a dictionary, or ``None`` if the request fails
        or the response cannot be parsed as valid YAML.

    Examples
    --------
    >>> data = load()
    >>> data["projects"][0]["name"]
    'numpy'
    """
    url = "https://raw.githubusercontent.com/lukasmasuch/best-of-python/main/projects.yaml"
    
    parsed_yaml = None
    
    try:
    
        response = requests.get(url)
        
        response.raise_for_status()
        
        text = response.text
        
        parsed_yaml = yaml.safe_load(text)
        
        parsed_yaml["projects"] = [p for p in parsed_yaml["projects"] if not p.get("resource")]
    
    except (RequestException, YAMLError) as e:
        logger.error(e)
    
    return parsed_yaml