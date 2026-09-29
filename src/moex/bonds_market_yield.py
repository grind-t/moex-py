from typing import TypedDict

import httpx

from .core.fetch import moex_fetch


class MoexBondMarketYield(TypedDict):
    SECID: str
    BOARDID: str
    PRICE: float
    YIELDDATE: str
    ZCYCMOMENT: str
    YIELDDATETYPE: str
    EFFECTIVEYIELD: float
    DURATION: float
    ZSPREADBP: float
    GSPREADBP: float
    WAPRICE: float
    EFFECTIVEYIELDWAPRICE: float
    DURATIONWAPRICE: float
    IR: float
    ICPI: float
    BEI: float
    CBR: float
    YIELDTOOFFER: float
    YIELDLASTCOUPON: float
    TRADEMOMENT: str
    SEQNUM: int
    SYSTIME: str


async def get_moex_bonds_market_yield(
    *, client: httpx.AsyncClient | None = None
) -> list[MoexBondMarketYield]:
    return await moex_fetch(
        "engines/stock/markets/bonds/securities.json",
        "marketdata_yields",
        client=client,
    )
