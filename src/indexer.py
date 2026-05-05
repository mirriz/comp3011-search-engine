import re
from collections import defaultdict

class InvertedIndex:
    """
    Builds and manages an inverted index storing word frequencies and positions.
    """
    def __init__(self):
        # Structure: { word: { url: { 'frequency': int, 'positions': [int, int] } } }
        self.index = defaultdict(lambda: defaultdict(lambda: {'frequency': 0, 'positions': []}))

    def _tokenize(self, text: str) -> list[str]:
        """
        Cleans text by converting to lowercase and removing punctuation.
        Returns a list of words.
        """
        # Convert to lowercase to ensure case-insensitive search
        text = text.lower()
        # Find all alphanumeric sequences (words)
        words = re.findall(r'\b[a-z0-9]+\b', text)
        return words

    def add_document(self, url: str, content: str):
        """
        Processes a document's content and adds its words to the inverted index.
        """
        words = self._tokenize(content)
        
        for position, word in enumerate(words):
            self.index[word][url]['frequency'] += 1
            self.index[word][url]['positions'].append(position)

    def get_index(self) -> dict:
        """Returns the built index as a standard dictionary."""
        # Convert the defaultdicts back to standard dicts for clean storage later
        return {word: dict(urls) for word, urls in self.index.items()}