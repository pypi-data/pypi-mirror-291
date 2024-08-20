import re

from google.protobuf.json_format import MessageToDict
from pydantic import BaseModel

from concave.internal.codebase.search.symbol.index import read_scip, parse_range
from concave.internal.codebase.search.symbol.scip import Symbol
import concave.internal.codebase.search.symbol.proto.scip_pb2 as pb


class SearchSymbolResults(BaseModel):
    name: str
    type: str
    namespace: str
    # [start_line, start_char, end_line, end_char]
    enclosing_start_line: int
    enclosing_start_char: int
    enclosing_end_line: int
    enclosing_end_char: int

def str_to_tokens(s):
    tokens = re.split("[./()_`:#]", s)
    return [t for t in tokens if t]

def match_keys(symbol, keys):
    for k in keys:
        if k in symbol:
            return True
    return False


class SymbolSearcher:
    def __init__(self, content):
        self.index = pb.Index.FromString(content)
        self._debug = MessageToDict(self.index)

    def scan_occurrences(self, occurrences, keys, filter_types):
        results = []
        for o in occurrences:
            if o.symbol_roles != pb.SymbolRole.Definition:
                continue
            symbol = Symbol(o.symbol)
            if match_keys(symbol.name, keys):
                if filter_types and symbol.type not in filter_types:
                    continue

                r = parse_range(o.enclosing_range)
                if not len(r) == 4:
                    raise ValueError(f"{MessageToDict(o)}, Invalid enclosing_range: {r}")

                results.append(SearchSymbolResults(
                    name=symbol.name,
                    type=symbol.type,
                    namespace=symbol.namespace,
                    enclosing_start_line=r[0],
                    enclosing_start_char=r[1],
                    enclosing_end_line=r[2],
                    enclosing_end_char=r[3]
                ))
        return results

    def search_symbols(self, keys, filter_path, filter_types=None):
        results = []
        for doc in self.index.documents:
            if doc.relative_path == filter_path:
                results.extend(
                    self.scan_occurrences(doc.occurrences, keys, filter_types)
                )
        return results

    def all_src_symbols(self):
        symbols = []
        for doc in self.index.documents:
            if doc.relative_path.startswith("test"):
                continue

            for s in doc.symbols:
                if s.symbol.startswith("local"):
                    continue
                symbols.append(s.symbol)

        return symbols

    def all_src_tokens(self):
        tokens = set()
        symbols = self.all_src_symbols()
        for s in symbols:
            tokens.update(str_to_tokens(s))
        return list(tokens)
