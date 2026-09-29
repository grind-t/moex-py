from typing import Literal, TypedDict

import httpx

from .core.fetch import moex_fetch


class MoexBondAmortization(TypedDict):
    isin: str
    name: str
    issuevalue: int
    amortdate: str
    facevalue: float
    initialfacevalue: float
    faceunit: str
    valueprc: float
    value: float
    value_rub: float
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
    return await moex_fetch(
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
