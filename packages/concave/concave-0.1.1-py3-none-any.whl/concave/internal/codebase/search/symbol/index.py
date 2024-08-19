from os.path import basename

from google.protobuf.json_format import MessageToDict
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

import concave.internal.codebase.search.symbol.proto.scip_pb2 as pb
from concave.internal.codebase.search.symbol.db import Occurrences, SymbolInfo


def parse_range(range):
    if len(range) == 3:
        return range[0], range[1], range[0], range[2]
    return range


def parse_occurrence(occurrence: pb.Occurrence, doc: pb.Document):
    r = parse_range(occurrence.range)
    symbol = occurrence.symbol
    if symbol.startswith("scip-python"):
        parts = symbol.split(" ")
        description = parts[4]
        if "/" not in description:
            print(MessageToDict(doc))
            print(MessageToDict(occurrence))
            raise ValueError(f"Unknown description: {description}")
        namespace, name_with_type = description.split("/")
        return Occurrences(
            symbol=occurrence.symbol,
            filename=basename(doc.relative_path),
            relative_path=doc.relative_path,
            language=doc.language,
            lib=parts[2],
            lib_version=parts[3],
            namespace=namespace,
            name_with_type=name_with_type,
            # name=doc.name,
            # type=doc.type,
            enclosing_range=str(occurrence.enclosing_range),
            role=pb.SymbolRole.Name(occurrence.symbol_roles),
            start_line=r[0],
            start_char=r[1],
            end_line=r[2],
            end_char=r[3],
        )
    if symbol.startswith("local"):
        return Occurrences(
            symbol=occurrence.symbol,
            filename=basename(doc.relative_path),
            relative_path=doc.relative_path,
            language=doc.language,
            lib="",
            lib_version="",
            namespace="local",
            name_with_type=occurrence.symbol,
            role=pb.SymbolRole.Name(occurrence.symbol_roles),
            start_line=r[0],
            start_char=r[1],
            end_line=r[2],
            end_char=r[3],
        )
    print(MessageToDict(doc))
    print(MessageToDict(occurrence))
    raise ValueError(f"Unknown symbol: {symbol}")


def read_scip(file_path: str) -> pb.Index:
    with open(file_path, "rb") as f:
        return pb.Index.FromString(f.read())


def parse_scip(file_path: str):
    occurrences = []
    symbols = []

    index = read_scip(file_path)
    for doc in index.documents:
        for o in doc.occurrences:
            occurrences.append(parse_occurrence(o, doc))
        for s in doc.symbols:
            symbols.append(SymbolInfo(
                symbol=s.symbol,
                relative_path=doc.relative_path,
                documentation="\n".join(s.documentation),
                filename=basename(doc.relative_path)
            ))

    for s in index.external_symbols:
        symbols.append(SymbolInfo(
            symbol=s.symbol,
            documentation="\n".join(s.documentation),
        ))

    return {
        "occurrences": occurrences,
        "symbols": symbols,
        "index": index
    }


def create_index_db(file_path: str, output_path: str = "db.sqlite"):
    scip_index = parse_scip(file_path)
    engine = create_engine(f"sqlite:///{output_path}")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all(scip_index["occurrences"])
        session.add_all(scip_index["symbols"])
        session.commit()
