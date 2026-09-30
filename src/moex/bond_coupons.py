from datetime import date
from typing import Literal

import httpx
from pydantic import BaseModel, Field

from .core.fetch import moex_fetch


class MoexBondCoupon(BaseModel):
    # None for some old (1990s) bonds.
    isin: str | None = Field(pattern=r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$")
    name: str = Field(min_length=1)
    # Not always whole (e.g. gold-linked bonds); 0 for some structured bonds.
    issuevalue: float | None = Field(ge=0)
    coupondate: date
    recorddate: date | None
    startdate: date | None
    initialfacevalue: float | None = Field(gt=0)
    # 0 for some fully amortized bonds.
    facevalue: float = Field(ge=0)
    faceunit: str = Field(pattern=r"^[A-Z]{3}$")
    # None when the payment amount is not known yet.
    value: float | None = Field(gt=0)
    # Annualized, so may exceed 100 for short-period structured bonds.
    valueprc: float | None = Field(gt=0)
    value_rub: float | None = Field(gt=0)
    secid: str = Field(min_length=1)
    primary_boardid: str | None = Field(pattern=r"^[A-Z0-9]{4}$")


async def get_moex_bond_coupons(
    *,
    lang: Literal["ru", "en"] | None = None,
    from_: str | None = None,
    till: str | None = None,
    limit: Literal[5, 10, 20, 100] | None = None,
    start: int | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[MoexBondCoupon]:
    rows = await moex_fetch(
        "statistics/engines/stock/markets/bonds/bondization.json",
        "coupons",
        {"lang": lang, "from": from_, "till": till, "limit": limit, "start": start},
        client,
    )
    return [MoexBondCoupon.model_validate(row) for row in rows]
