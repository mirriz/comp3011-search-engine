import pytest
import requests_mock
from unittest.mock import patch
from src.crawler import WebCrawler

class TestWebCrawler:
    
    @pytest.fixture
    def crawler(self):
        return WebCrawler("https://quotes.toscrape.com/")

    @patch('time.sleep') # This intercepts time.sleep so our test doesn't actually wait 6 seconds
    def test_fetch_page_success_and_politeness(self, mock_sleep, crawler):
        test_url = "https://quotes.toscrape.com/page/1/"
        mock_html = "<html><body><h1>Test Quote</h1></body></html>"

        # Use requests_mock to simulate the website's response
        with requests_mock.Mocker() as m:
            m.get(test_url, text=mock_html, status_code=200)
            
            result = crawler._fetch_page(test_url)
            
            # 1. Assert we got the right HTML back
            assert result == mock_html
            
            # 2. CRITICAL: Assert the 6-second politeness window was enforced
            mock_sleep.assert_called_once_with(6.0)

    def test_fetch_page_handles_404(self, crawler):
        test_url = "https://quotes.toscrape.com/does-not-exist"
        
        with requests_mock.Mocker() as m:
            m.get(test_url, status_code=404)
            
            result = crawler._fetch_page(test_url)
            
            # Assert the crawler gracefully returns None on a 404 error
            assert result is None

    @patch('time.sleep')
    def test_crawl_pagination_and_extraction(self, mock_sleep, crawler):
        """Tests that the crawler parses content and follows pagination."""
        base_url = "https://quotes.toscrape.com/"
        page_2_url = "https://quotes.toscrape.com/page/2/"
        
        # Mock HTML for page 1 (contains a 'next' link)
        html_page_1 = """
        <html>
            <body>
                <div class="quote">
                    <span class="text">"First quote"</span>
                    <small class="author">Author One</small>
                </div>
                <li class="next"><a href="/page/2/">Next</a></li>
            </body>
        </html>
        """
        
        # Mock HTML for page 2 (NO 'next' link)
        html_page_2 = """
        <html>
            <body>
                <div class="quote">
                    <span class="text">"Second quote"</span>
                    <small class="author">Author Two</small>
                </div>
            </body>
        </html>
        """
        
        with requests_mock.Mocker() as m:
            # Map the mock HTML to the URLs
            m.get(base_url, text=html_page_1)
            m.get(page_2_url, text=html_page_2)
            
            # Run the crawler
            result = crawler.crawl()
            
            # Assertions
            assert len(result) == 2 # Should have scraped exactly 2 pages
            assert base_url in result
            assert page_2_url in result
            assert '"First quote" Author One' in result[base_url]
            assert '"Second quote" Author Two' in result[page_2_url]
            assert mock_sleep.call_count == 2 # Should have slept twice