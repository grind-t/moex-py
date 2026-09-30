from typing import Annotated, Literal

import httpx
from pydantic import BaseModel, BeforeValidator, Field

from .core.fetch import moex_fetch
from .core.types import Engine, Market

# ISS sends "" (and for isin even "None") instead of null for some indices,
# currencies and old state bonds.
MaybeStr = Annotated[
    str | None, BeforeValidator(lambda v: None if v in ("", "None") else v)
]


# Issuer fields (emitent_*), isin and regnumber are None for derivatives,
# indices, currencies and commodities, and for some foreign securities.
class MoexSecurity(BaseModel):
    # \w: an old commodity future has a Cyrillic letter ("R1Н4").
    secid: str = Field(pattern=r"^[\w.+-]+$")
    # None for some delisted securities and futures spreads.
    shortname: str | None = Field(min_length=1)
    regnumber: MaybeStr = Field(min_length=1)
    name: str | None = Field(min_length=1)
    # The check digit is missing for a few bond indices.
    isin: MaybeStr = Field(pattern=r"^[A-Z]{2}[A-Z0-9]{9}[0-9]?$")
    # None for some futures spreads.
    is_traded: bool | None
    emitent_id: int | None = Field(gt=0)
    emitent_title: str | None = Field(min_length=1)
    # Not always a real INN: foreign issuers have short registry numbers.
    emitent_inn: str | None = Field(pattern=r"^[0-9]{1,12}$")
    # Leading zeros are sometimes dropped.
    emitent_okpo: str | None = Field(pattern=r"^[0-9]{5,8}$")
    # Open sets, e.g. "common_share" in "stock_shares", "option" in
    # "futures_options".
    type: str = Field(pattern=r"^[a-z]+(_[a-z]+)*$")
    group: str = Field(pattern=r"^[a-z]+(_[a-z]+)*$")
    # None for some delisted securities (mostly bonds); 3 letters for a few old
    # boards ("FOB", "BKT").
    primary_boardid: str | None = Field(pattern=r"^[A-Z0-9]{3,4}$")
    # Only set for some stock market securities (shares, bonds, funds).
    marketprice_boardid: str | None = Field(pattern=r"^[A-Z0-9]{4}$")


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
    rows = await moex_fetch(
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
    return [MoexSecurity.model_validate(row) for row in rows]
