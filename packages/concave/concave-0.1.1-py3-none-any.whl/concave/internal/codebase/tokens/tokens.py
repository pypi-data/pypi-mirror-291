import re

from sqlalchemy import create_engine
from sqlmodel import Session, select

from concave.internal.codebase.search.symbol.db import SymbolInfo


# input: `src._pytest.hookspec`/pytest_make_collect_report().
# output: ["src", "_pytest", "hookspec", "pytest_make_collect_report"]
def str_to_tokens(s):
    # return s.split(".").split("/").split("(").split(")").split("`")
    tokens = re.split("[./()_`:#]", s)
    #     remove empty tokens
    return [t for t in tokens if t]


class TokensIndexer:
    def __init__(self, db_file):
        self.engine = create_engine(f"sqlite:///{db_file}")

    def _get_symbols(self):
        with Session(self.engine) as session:
            rows = session.exec(select(SymbolInfo)).all()

        results = []
        for r in rows:
            symbol = r.symbol
            if not r.relative_path:
                continue
            if r.relative_path.startswith("test"):
                continue
            if symbol.startswith("local"):
                continue
            symbol = symbol.split(" ")[-1]
            results.append(symbol)
        return results

    def tokens(self):
        symbols = self._get_symbols()
        results = set()
        for s in symbols:
            results.update(str_to_tokens(s))
        return results
