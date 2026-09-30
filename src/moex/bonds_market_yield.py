from datetime import date, datetime
from typing import Literal

import httpx
from pydantic import BaseModel, Field

from .core.fetch import moex_fetch


class MoexBondMarketYield(BaseModel):
    # Not unique: a bond may trade on several boards.
    SECID: str = Field(min_length=1)
    BOARDID: str = Field(pattern=r"^[A-Z0-9]{4}$")
    # Price the yields below are computed from; set even for bonds that did not
    # trade today.
    PRICE: float = Field(gt=0)
    # None for bonds without a maturity date (perpetuals).
    YIELDDATE: date | None
    # Timestamp of the zero-coupon yield curve used in the calculation.
    ZCYCMOMENT: datetime
    YIELDDATETYPE: Literal["MATDATE", "OFFER", "MBS"]
    # No bounds: ranges from -100s to eight-figure values for distressed bonds.
    # None when the yield cannot be computed (e.g. perpetuals).
    EFFECTIVEYIELD: float | None
    # In days.
    DURATION: int | None = Field(ge=0)
    # In basis points; no bounds.
    ZSPREADBP: int | None
    GSPREADBP: int | None
    # None when the bond has not traded today.
    WAPRICE: float | None = Field(gt=0)
    EFFECTIVEYIELDWAPRICE: float | None
    DURATIONWAPRICE: int | None = Field(ge=0)
    # Implied rates, set only for floaters and linkers; no bounds.
    IR: float | None
    ICPI: float | None
    BEI: float | None
    # Always null in live data.
    CBR: None
    # Set only when YIELDDATETYPE is OFFER.
    YIELDTOOFFER: float | None
    YIELDLASTCOUPON: float | None
    # Last trade time; 23:59:59 of the last trading day when the bond has not
    # traded today.
    TRADEMOMENT: datetime
    SEQNUM: int = Field(gt=0)
    SYSTIME: datetime


async def get_moex_bonds_market_yield(
    *, client: httpx.AsyncClient | None = None
) -> list[MoexBondMarketYield]:
    rows = await moex_fetch(
        "engines/stock/markets/bonds/securities.json",
        "marketdata_yields",
        client=client,
    )
    return [MoexBondMarketYield.model_validate(row) for row in rows]
