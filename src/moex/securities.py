from typing import Literal, TypedDict

import httpx

from .core.fetch import moex_fetch
from .core.types import Engine, Market


class MoexSecurity(TypedDict):
    id: int
    secid: str
    shortname: str
    regnumber: str
    name: str
    isin: str
    is_traded: int
    emitent_id: int
    emitent_title: str
    emitent_inn: str
    emitent_okpo: str
    gosreg: str
    type: str
    group: str
    primary_boardid: str
    marketprice_boardid: str


async def get_moex_securities(
    *,
    q: str | None = None,
    lang: Literal["ru", "en"] | None = None,
    engine: Engine | None = None,
    is_trading: Literal[1, 0] | None = None,
    market: Market | None = None,
    group_by: Literal["group", "type"] | None = None,
    limit: Literal[5, 10, 20, 100] | None = None,
    group_by_filter: str | None = None,
    start: int | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[MoexSecurity]:
    return await moex_fetch(
        "securities.json",
        "securities",
        {
            "q": q,
            "lang": lang,
            "engine": engine,
            "is_trading": is_trading,
            "market": market,
            "group_by": group_by,
            "limit": limit,
            "group_by_filter": group_by_filter,
            "start": start,
        },
        client,
    )
