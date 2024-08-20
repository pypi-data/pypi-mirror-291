class SymbolType:
    CLASS = "CLASS"
    METHOD = "METHOD"
    MODULE_INIT = "MODULE_INIT"
    MODULE_INIT_META = "MODULE_INIT_META"
    PARAMETER = "PARAMETER"

    # in python, might be a variable ?
    TERM = "TERM"

    LOCAL = "LOCAL"

    UNKNOWN = "UNKNOWN"


# https://github.com/sourcegraph/scip-python/blob/scip/packages/pyright-scip/src/symbols.ts#L33-L79
def name_to_type(name: str):
    if name.startswith("local"):
        return SymbolType.LOCAL

    if name.endswith("__init__"):
        return SymbolType.MODULE_INIT
    if name.endswith("__init__:"):
        return SymbolType.MODULE_INIT_META
    if name.endswith("#"):
        return SymbolType.CLASS
    if name.endswith(")."):
        return SymbolType.METHOD
    if name.endswith(")"):
        return SymbolType.PARAMETER
    if name.endswith("."):
        return SymbolType.TERM
    return SymbolType.UNKNOWN


class Symbol:

    def __init__(self, symbol: str):
        self._symbol = symbol
        if symbol.startswith("local"):
            self.namespace = "local"
            self.name = symbol.split(" ")[1]
            self.type = SymbolType.LOCAL
            return

        parts = symbol.split(" ")
        description = parts[4]
        if "/" not in description:
            raise ValueError(f"Unknown description: {description}")
        self.namespace, self.name = description.split("/")
        self.type = name_to_type(symbol)
