import cmd
from crawler import WebCrawler
from indexer import InvertedIndex
from search import SearchEngine

class SearchEngineShell(cmd.Cmd):
    intro = '\nWelcome to the COMP3011 Search Engine Tool.\nType help or ? to list commands.\n'
    prompt = '> '

    def __init__(self):
        super().__init__()
        self.indexer = InvertedIndex()
        self.index_file = 'data/index.json'
        self.base_url = "https://quotes.toscrape.com/"

    def do_build(self, arg):
        """
        build
        Crawls the website, builds the index, and saves it to the file system.
        """
        print(f"Initializing crawler for {self.base_url}...")
        crawler = WebCrawler(self.base_url)
        pages = crawler.crawl()
        
        print("\nBuilding inverted index...")
        self.indexer.index.clear() # Clear existing index before rebuilding
        for url, content in pages.items():
            self.indexer.add_document(url, content)
            
        self.indexer.save(self.index_file)

    def do_load(self, arg):
        """
        load
        Loads the previously built index from the file system.
        """
        self.indexer.load(self.index_file)

    def do_print(self, arg):
        """
        print <word>
        Prints the inverted index for a particular word.
        """
        if not arg:
            print("Please provide a word to search for. Example: print nonsense")
            return
            
        # TODO: Implement print logic
        print(f"Searching for word: {arg}")

    def do_find(self, arg):
        """
        find <query phrase>
        Finds a given query phrase in the index and returns matching pages.
        """
        if not arg:
            print("Please provide a query. Example: find good friends")
            return
            
        # TODO: Implement advanced search logic (TF-IDF ranking)
        print(f"Finding pages for query: {arg}")

    def do_exit(self, arg):
        """Exit the search engine shell."""
        print("Goodbye!")
        return True
    
    def do_print(self, arg):
        """
        print <word>
        Prints the inverted index for a particular word.
        """
        if not arg:
            print("Please provide a word to search for. Example: print nonsense")
            return
            
        searcher = SearchEngine(self.indexer.get_index())
        stats = searcher.get_word_stats(arg)
        
        if not stats:
            print(f"The word '{arg}' was not found in the index.")
        else:
            print(f"Index for '{arg}':")
            for url, data in stats.items():
                print(f"  URL: {url}")
                print(f"    Frequency: {data['frequency']}")
                print(f"    Positions: {data['positions']}")

    def do_find(self, arg):
        """
        find <query phrase>
        Finds a given query phrase in the index and returns ranked pages.
        """
        if not arg:
            print("Please provide a query. Example: find good friends")
            return
            
        searcher = SearchEngine(self.indexer.get_index())
        suggestion = searcher.suggest_query(arg)
        if suggestion:
            print(f"  [!] Did you mean: '{suggestion}'?")
        results = searcher.find_query(arg)
        
        if not results:
            print(f"No pages found containing the query: '{arg}'")
        else:
            print(f"Found {len(results)} pages matching '{arg}' (Ranked by TF-IDF):")
            for rank, (url, score) in enumerate(results, 1):
                # Format score to 4 decimal places for clean output
                print(f"  {rank}. {url} (Score: {score:.4f})")

if __name__ == '__main__':
    SearchEngineShell().cmdloop()