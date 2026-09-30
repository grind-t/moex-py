from datetime import date
from typing import Annotated, Literal

import httpx
from pydantic import BaseModel, BeforeValidator, Field

from .core.fetch import moex_fetch

# ISS sends "0000-00-00" instead of null for a missing date.
MaybeDate = Annotated[
    date | None, BeforeValidator(lambda v: None if v == "0000-00-00" else v)
]


class MoexBond(BaseModel):
    SECID: str = Field(min_length=1)
    BOARDID: str = Field(pattern=r"^[A-Z0-9]{4}$")
    SHORTNAME: str = Field(min_length=1)
    # None when the bond has not traded yet (or for a while).
    PREVWAPRICE: float | None = Field(gt=0)
    # No bounds: ranges from -100 to six-figure values for distressed bonds.
    YIELDATPREVWAPRICE: float | None
    COUPONVALUE: float = Field(ge=0)
    # None for bonds without a coupon schedule (mostly structured bonds).
    NEXTCOUPON: MaybeDate
    ACCRUEDINT: float = Field(ge=0)
    PREVPRICE: float | None = Field(gt=0)
    LOTSIZE: int = Field(gt=0)
    # Not always whole: amortized or indexed bonds have fractional face values.
    FACEVALUE: float = Field(gt=0)
    BOARDNAME: str = Field(min_length=1)
    STATUS: Literal["A", "N"]
    # None for perpetual bonds and some bonds with a call option.
    MATDATE: MaybeDate
    DECIMALS: int = Field(ge=0)
    # 0 for bonds without periodic coupons.
    COUPONPERIOD: int = Field(ge=0)
    ISSUESIZE: int = Field(gt=0)
    PREVLEGALCLOSEPRICE: float | None = Field(gt=0)
    # None when the bond has no previous trading day.
    PREVDATE: MaybeDate
    SECNAME: str = Field(min_length=1)
    REMARKS: str | None = Field(pattern=r"^[A-Z]+$")
    MARKETCODE: str = Field(pattern=r"^[A-Z]{4}$")
    INSTRID: str = Field(pattern=r"^[A-Z]{4}$")
    # Always null in live data.
    SECTORID: None
    MINSTEP: float = Field(gt=0)
    FACEUNIT: str = Field(pattern=r"^[A-Z]{3}$")
    BUYBACKPRICE: float | None = Field(gt=0)
    BUYBACKDATE: MaybeDate
    ISIN: str = Field(pattern=r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$")
    LATNAME: str = Field(min_length=1)
    REGNUMBER: str | None = Field(min_length=1)
    CURRENCYID: str = Field(pattern=r"^[A-Z]{3}$")
    ISSUESIZEPLACED: int | None = Field(gt=0)
    LISTLEVEL: Literal[1, 2, 3]
    SECTYPE: str = Field(pattern=r"^[0-9A-Z]$")
    # None when the rate is not known yet (e.g. floaters, structured bonds).
    COUPONPERCENT: float | None = Field(gt=0)
    OFFERDATE: date | None
    SETTLEDATE: date
    LOTVALUE: float = Field(gt=0)
    FACEVALUEONSETTLEDATE: float | None = Field(gt=0)
    CALLOPTIONDATE: date | None
    PUTOPTIONDATE: date | None
    DATEYIELDFROMISSUER: date | None
    BONDTYPE: str | None = Field(min_length=1)
    BONDSUBTYPE: Literal[
        "До погашения", "До оферты (put)", "До оферты (call)", "Бессрочные"
    ]
    COUPON_DETAILS: str | None = Field(min_length=1)
    FACEVALUE_TYPE: Literal["Фиксированный", "Индексированный"]


async def get_moex_bonds(
    *,
    primary_board: Literal[1, 0] | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[MoexBond]:
    rows = await moex_fetch(
        "engines/stock/markets/bonds/securities.json",
        "securities",
        {"primary_board": primary_board},
        client,
    )
    return [MoexBond.model_validate(row) for row in rows]
