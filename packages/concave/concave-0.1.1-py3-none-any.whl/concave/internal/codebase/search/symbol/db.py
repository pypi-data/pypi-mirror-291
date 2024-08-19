from sqlmodel import Field, SQLModel, create_engine


class SymbolInfo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    symbol: str
    filename: str | None
    relative_path: str | None
    documentation: str | None


class Occurrences(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    filename: str
    relative_path: str

    symbol: str
    language: str
    lib: str | None
    lib_version: str | None = None
    namespace: str | None = None
    name: str | None = None
    name_with_type: str
    type: str | None
    role: str
    start_line: int
    start_char: int
    end_line: int
    end_char: int

    enclosing_range: str | None = None