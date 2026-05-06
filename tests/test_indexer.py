import pytest
from src.indexer import InvertedIndex
import os
import json

class TestInvertedIndex:
    
    @pytest.fixture
    def indexer(self):
        return InvertedIndex()

    def test_tokenize_cleans_text(self, indexer):
        """Tests that punctuation is removed and text is lowercase."""
        raw_text = 'Hello, World! "Good" friends... 123.'
        expected_tokens = ['hello', 'world', 'good', 'friends', '123']
        
        tokens = indexer._tokenize(raw_text)
        assert tokens == expected_tokens

    def test_add_document_builds_correct_statistics(self, indexer):
        """Tests that frequency and positions are accurately recorded."""
        url = "https://quotes.toscrape.com/page/1/"
        content = "To be or not to be"
        
        indexer.add_document(url, content)
        index = indexer.get_index()
        
        # 'to' appears at index 0 and 4
        assert 'to' in index
        assert index['to'][url]['frequency'] == 2
        assert index['to'][url]['positions'] == [0, 4]
        
        # 'be' appears at index 1 and 5
        assert 'be' in index
        assert index['be'][url]['frequency'] == 2
        assert index['be'][url]['positions'] == [1, 5]
        
        # 'not' appears at index 3
        assert 'not' in index
        assert index['not'][url]['frequency'] == 1
        assert index['not'][url]['positions'] == [3]

    def test_multiple_documents(self, indexer):
        """Tests that the index correctly separates data from different URLs."""
        url1 = "http://site.com/1"
        url2 = "http://site.com/2"
        
        indexer.add_document(url1, "apple orange")
        indexer.add_document(url2, "apple banana apple")
        
        index = indexer.get_index()
        
        # Apple should be in both URLs
        assert 'apple' in index
        assert index['apple'][url1]['frequency'] == 1
        assert index['apple'][url2]['frequency'] == 2

    def test_save_and_load(self, indexer, tmp_path):
        """Tests that the index can be saved to and loaded from a JSON file."""
        # Setup mock data
        indexer.add_document("url1", "test data")
        
        # Use pytest's built-in tmp_path fixture for safe file testing
        test_file = tmp_path / "test_index.json"
        
        # Test saving
        indexer.save(str(test_file))
        assert os.path.exists(test_file)
        
        # Test loading into a new indexer instance
        new_indexer = InvertedIndex()
        new_indexer.load(str(test_file))
        
        assert 'test' in new_indexer.index
        assert 'url1' in new_indexer.index['test']