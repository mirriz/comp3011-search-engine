import math
import re

class SearchEngine:
    """
    Handles querying the inverted index using TF-IDF ranking.
    """
    def __init__(self, index_data: dict):
        self.index = index_data
        self.total_documents = self._calculate_total_documents()

    def _calculate_total_documents(self) -> int:
        """Determines the total number of unique URLs in the index."""
        unique_urls = set()
        for urls in self.index.values():
            unique_urls.update(urls.keys())
        return max(1, len(unique_urls)) # Prevent division by zero

    def _tokenize(self, text: str) -> list[str]:
        """Ensures query uses the same tokenization as the indexer."""
        return re.findall(r'\b[a-z0-9]+\b', text.lower())

    def get_word_stats(self, word: str) -> dict:
        """Returns the raw index data for a specific word (for the 'print' command)."""
        word = word.lower()
        return self.index.get(word, {})

    def find_query(self, query: str) -> list[tuple[str, float]]:
        """
        Finds pages matching the query and ranks them using TF-IDF.
        Returns a sorted list of tuples: [(url, score), ...]
        """
        query_words = self._tokenize(query)
        if not query_words:
            return []

        document_scores = {}

        for word in query_words:
            if word not in self.index:
                continue # Word doesn't exist in our index

            word_data = self.index[word]
            document_frequency = len(word_data)
            
            # Calculate IDF: log(Total Documents / Documents containing word)
            idf = math.log(self.total_documents / document_frequency)

            # Calculate TF-IDF for each document containing this word
            for url, stats in word_data.items():
                # For simplicity, we use raw frequency for TF
                tf = stats['frequency']
                tf_idf_score = tf * idf
                
                # Accumulate scores for multi-word queries
                if url in document_scores:
                    document_scores[url] += tf_idf_score
                else:
                    document_scores[url] = tf_idf_score

        # Sort documents by score in descending order
        sorted_results = sorted(document_scores.items(), key=lambda item: item[1], reverse=True)
        return sorted_results