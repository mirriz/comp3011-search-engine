import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class WebCrawler:
    """
    A web crawler designed to scrape quotes.toscrape.com.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.visited_urls = set()
        self.pages_data = []
        self.politeness_delay = 6.0  # Strict 6-second window

    def _fetch_page(self, url: str) -> str | None:
        """Fetches the HTML content of a given URL with politeness enforced."""
        print(f"Fetching: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Enforce the politeness window
            print(f"Sleeping for {self.politeness_delay} seconds...")
            time.sleep(self.politeness_delay)
            
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def crawl(self) -> list:
        """Starts the crawling process from the base URL."""
        # TODO: Implement the traversal logic using BeautifulSoup
        pass