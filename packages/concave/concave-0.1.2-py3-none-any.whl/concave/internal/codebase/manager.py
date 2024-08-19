import os


from concave.internal.codebase.search.full_text.full_text import FullTextSearcher
from concave.internal.codebase.search.symbol.searcher import SymbolSearcher


class CodeSearchManager:

    def __init__(self, path, zoekt_endpoint="http://localhost:6070"):
        self.path = path
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path {path} does not exist")

        self._symbol_searcher = SymbolSearcher(os.path.join(path, "index", "scip"))
        self._full_text_searcher = FullTextSearcher(zoekt_endpoint)
        # self._vector_searcher = VectorSearcher(os.path.join(path, "index", "vector"))

    def symbol_search(self, query, **kwargs):
        return self._symbol_searcher.search(query)

    def full_text_search(self, query, **kwargs):
        return self._full_text_searcher.search(query, **kwargs)

    # def vector_search(self, query, **kwargs):
    #     return self._vector_searcher.search(query, **kwargs)
