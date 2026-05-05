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