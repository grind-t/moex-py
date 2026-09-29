from typing import Literal, TypedDict

import httpx

from .core.fetch import moex_fetch


class MoexBondCoupon(TypedDict):
    isin: str
    name: str
    issuevalue: int
    coupondate: str
    recorddate: str
    startdate: str
    initialfacevalue: float
    facevalue: float
    faceunit: str
    value: float
    valueprc: float
    value_rub: float
    secid: str
    primary_boardid: str


async def get_moex_bond_coupons(
    *,
    lang: Literal["ru", "en"] | None = None,
    from_: str | None = None,
    till: str | None = None,
    limit: Literal[5, 10, 20, 100] | None = None,
    start: int | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[MoexBondCoupon]:
    return await moex_fetch(
        "statistics/engines/stock/markets/bonds/bondization.json",
        "coupons",
        {"lang": lang, "from": from_, "till": till, "limit": limit, "start": start},
        client,
    )
