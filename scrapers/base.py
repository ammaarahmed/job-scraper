import requests
from typing import Optional, Dict, Any

class BaseScraper:
    """Simple base scraper supporting optional proxies."""

    def __init__(self, proxies: Optional[Dict[str, str]] = None):
        self.session = requests.Session()
        self.proxies = proxies or {}

    def get(self, url: str, **kwargs) -> requests.Response:
        """Perform GET request using the current session and proxies."""
        response = self.session.get(url, proxies=self.proxies, **kwargs)
        response.raise_for_status()
        return response

    def post(self, url: str, data: Any = None, json: Any = None, **kwargs) -> requests.Response:
        """Perform POST request using the current session and proxies."""
        response = self.session.post(url, data=data, json=json, proxies=self.proxies, **kwargs)
        response.raise_for_status()
        return response
