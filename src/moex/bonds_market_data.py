from typing import TypedDict

import httpx

from .core.fetch import moex_fetch


class MoexBondMarketData(TypedDict):
    SECID: str
    BID: float
    OFFER: float
    SPREAD: float
    BIDDEPTHT: float
    OFFERDEPTHT: float
    OPEN: float
    LOW: float
    HIGH: float
    LAST: float
    LASTCHANGE: float
    LASTCHANGEPRCNT: float
    QTY: float
    VALUE: float
    YIELD: float
    VALUE_USD: float
    WAPRICE: float
    LASTCNGTOLASTWAPRICE: float
    WAPTOPREVWAPRICEPRCNT: float
    WAPTOPREVWAPRICE: float
    YIELDATWAPRICE: float
    YIELDTOPREVYIELD: float
    CLOSEYIELD: float
    CLOSEPRICE: float
    MARKETPRICETODAY: float
    MARKETPRICE: float
    LASTTOPREVPRICE: float
    NUMTRADES: int
    VOLTODAY: float
    VALTODAY: float
    VALTODAY_USD: float
    BOARDID: str
    TRADINGSTATUS: str
    UPDATETIME: str
    DURATION: float
    CHANGE: float
    TIME: str
    PRICEMINUSPREVWAPRICE: float
    LCURRENTPRICE: float
    LCLOSEPRICE: float
    MARKETPRICE2: float
    OPENPERIODPRICE: float
    SEQNUM: int
    SYSTIME: str
    VALTODAY_RUR: float
    IRICPICLOSE: float
    BEICLOSE: float
    CBRCLOSE: float
    YIELDTOOFFER: float
    YIELDLASTCOUPON: float
    TRADINGSESSION: str
    CALLOPTIONYIELD: float
    CALLOPTIONDURATION: float


async def get_moex_bonds_market_data(
    *, client: httpx.AsyncClient | None = None
) -> list[MoexBondMarketData]:
    return await moex_fetch(
        "engines/stock/markets/bonds/securities.json", "marketdata", client=client
    )
