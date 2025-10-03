import requests
import time
from typing import Any, Optional
from ..core.config import REQUEST_DELAY_SECONDS, DOFOCUS_API_BASE_URL

_session: Optional[requests.Session] = None

def _get_session() -> requests.Session:
    global _session
    if _session is None:
        s = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        s.mount("https://", adapter)
        s.mount("http://", adapter)
        _session = s
    return _session

def make_request(method: str, endpoint: str, **kwargs) -> Any:
    """Effectue une requête HTTP vers l'API avec gestion des délais et retries."""
    url = f"{DOFOCUS_API_BASE_URL}{endpoint}"
    session = _get_session()
    try:
        resp = session.request(method, url, timeout=15, **kwargs)
        resp.raise_for_status()
        # Respect delay between requests
        time.sleep(REQUEST_DELAY_SECONDS)
        return resp.json()
    except requests.exceptions.RequestException as e:
        # Remonter une erreur claire ; caller pourra logger/retry si nécessaire
        raise Exception(f"Erreur API pour {url}: {e}")
