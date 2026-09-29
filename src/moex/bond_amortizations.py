from datetime import date
from typing import Literal

import httpx
from pydantic import BaseModel

from .core.fetch import moex_fetch


class MoexBondAmortization(BaseModel):
    isin: str
    name: str
    issuevalue: int
    amortdate: date
    facevalue: float | None
    initialfacevalue: float
    faceunit: str
    valueprc: float | None
    value: float | None
    value_rub: float | None
    data_source: str
    secid: str
    primary_boardid: str


async def get_moex_bond_amortizations(
    id: str,
    *,
    lang: Literal["ru", "en"] | None = None,
    from_: str | None = None,
    till: str | None = None,
    limit: int | None = None,
    start: int | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[MoexBondAmortization]:
    rows = await moex_fetch(
        f"securities/{id}/bondization.json",
        "amortizations",
        {
            "lang": lang,
            "from": from_,
            "till": till,
            "limit": "unlimited" if limit is None else limit,
            "start": start,
        },
        client,
    )
    return [MoexBondAmortization.model_validate(row) for row in rows]
