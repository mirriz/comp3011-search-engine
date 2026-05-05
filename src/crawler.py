import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class WebCrawler:
    """
    A polite web crawler designed to scrape quotes.toscrape.com.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.visited_urls = set()
        self.pages_data = {} # Changed to dictionary to map URL -> Page Content
        self.politeness_delay = 6.0

    def _fetch_page(self, url: str) -> str | None:
        """Fetches the HTML content of a given URL with politeness enforced."""
        print(f"Fetching: {url}")
        try:
            response = requests.get(url, timeout=10) # Added timeout for defensive programming
            response.raise_for_status()
            
            print(f"Sleeping for {self.politeness_delay} seconds...")
            time.sleep(self.politeness_delay)
            
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def crawl(self) -> dict:
        """
        Crawls the website following pagination links.
        Returns a dictionary mapping URLs to their extracted text.
        """
        current_url = self.base_url
        
        while current_url and current_url not in self.visited_urls:
            html = self._fetch_page(current_url)
            if not html:
                break
                
            self.visited_urls.add(current_url)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract clean text (quotes and authors)
            page_content = []
            for quote_block in soup.find_all('div', class_='quote'):
                text = quote_block.find('span', class_='text').get_text(strip=True)
                author = quote_block.find('small', class_='author').get_text(strip=True)
                page_content.append(f"{text} {author}")
            
            self.pages_data[current_url] = " ".join(page_content)
            
            # Handle Pagination: Find the 'Next' button
            next_button = soup.find('li', class_='next')
            if next_button:
                next_link = next_button.find('a')['href']
                current_url = urljoin(self.base_url, next_link)
            else:
                current_url = None # End of pagination
                
        return self.pages_data