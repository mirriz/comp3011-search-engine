import pytest
from src.search import SearchEngine

class TestSearchEngine:
    
    @pytest.fixture
    def mock_index(self):
        # A small mock index with 3 documents
        return {
            'good': {
                'url1': {'frequency': 1, 'positions': [0]},
                'url2': {'frequency': 3, 'positions': [0, 5, 10]} # url2 has 'good' 3 times
            },
            'friends': {
                'url2': {'frequency': 1, 'positions': [6]},
                'url3': {'frequency': 1, 'positions': [0]}
            }
        }

    def test_calculate_total_documents(self, mock_index):
        searcher = SearchEngine(mock_index)
        assert searcher.total_documents == 3 # url1, url2, url3

    def test_get_word_stats(self, mock_index):
        searcher = SearchEngine(mock_index)
        stats = searcher.get_word_stats('good')
        assert 'url1' in stats
        assert 'url2' in stats
        
        # Test case insensitivity
        stats_upper = searcher.get_word_stats('GOOD')
        assert stats == stats_upper

    def test_find_query_ranking(self, mock_index):
        searcher = SearchEngine(mock_index)
        results = searcher.find_query("good")
        
        # url2 should rank higher than url1 because 'good' appears 3 times (higher TF)
        assert results[0][0] == 'url2'
        assert results[1][0] == 'url1'

    def test_multi_word_query(self, mock_index):
        searcher = SearchEngine(mock_index)
        results = searcher.find_query("good friends")
        
        # url2 has BOTH 'good' and 'friends', so it should definitely be top
        assert results[0][0] == 'url2'
    
    def test_suggest_query(self, mock_index):
        searcher = SearchEngine(mock_index)
        
        # 'goood' is misspelled, should suggest 'good'
        suggestion = searcher.suggest_query("goood")
        assert suggestion == "good"
        
        # Correctly spelled words should return None (no correction needed)
        assert searcher.suggest_query("friends") is None