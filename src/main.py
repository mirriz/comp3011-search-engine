import cmd
from crawler import WebCrawler
from indexer import InvertedIndex

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

if __name__ == '__main__':
    SearchEngineShell().cmdloop()