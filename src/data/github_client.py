from concurrent.futures import ThreadPoolExecutor
from loguru import logger
from requests.exceptions import RequestException
import requests
import os

def get_repo(github_id: str) -> dict | None:
    """Fetch repository metadata from the GitHub API.

    Uses the ``GITHUB_TOKEN`` environment variable for authentication when
    available, falling back to unauthenticated requests (60 req/h limit).

    Parameters
    ----------
    github_id : str
        Repository identifier in ``owner/repo`` format (e.g. ``"numpy/numpy"``).

    Returns
    -------
    dict or None
        GitHub API response as a dictionary, or ``None`` if the request fails.

    Examples
    --------
    >>> repo = get_repo("numpy/numpy")
    >>> repo["stargazers_count"]
    27000
    """
    token = os.getenv("GITHUB_TOKEN")
    
    headers = {
        "Authorization": f"Bearer {token}"
    } if token else None
    
    if github_id.count("/") == 1:
    
        owner, repo = github_id.split("/")
    else: 
        return None
    
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        
        response = requests.get(url, headers=headers, timeout=15)
        
        response.raise_for_status()
        
        stats_json = response.json()
        
        return stats_json
        
    except RequestException as e:
        logger.error(e)
        return None
    
def get_repos(github_ids: list) -> list[dict | None]:
    """Fetch repository metadata for multiple repos concurrently.

    Parameters
    ----------
    github_ids : list
        Repository identifiers in ``owner/repo`` format.

    Returns
    -------
    list of dict or None
        One entry per input repo; ``None`` for any that failed.
    """
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(get_repo, github_ids)
            
    return list(results)