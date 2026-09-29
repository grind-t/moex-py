from collections.abc import Mapping, Sequence
from typing import Any, TypeVar

T = TypeVar("T")


def parse_moex_block(block: Mapping[str, Sequence[Any]]) -> list[T]:
    columns = block["columns"]
    records = []
    for row in block["data"]:
        records.append(
            {column: row[i] if i < len(row) else None for i, column in enumerate(columns)}
        )
    return records  # type: ignore[return-value]
