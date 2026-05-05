import re
from collections import defaultdict
import json
import os

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
    
    def save(self, filepath: str):
        """Saves the compiled index to the file system using JSON."""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.get_index(), f, indent=4)
        print(f"Index successfully saved to {filepath}")

    def load(self, filepath: str):
        """Loads the index from the file system."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                
            # Reconstruct our defaultdict structure
            self.index.clear()
            for word, urls in loaded_data.items():
                for url, stats in urls.items():
                    self.index[word][url] = stats
            print(f"Index successfully loaded from {filepath}")
            
        except FileNotFoundError:
            print(f"Error: Could not find index file at {filepath}. Have you run 'build' yet?")
        except json.JSONDecodeError:
            print("Error: The index file is corrupted.")