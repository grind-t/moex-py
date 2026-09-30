from datetime import datetime, time

import httpx
from pydantic import BaseModel, Field

from .core.fetch import moex_fetch


class MoexBondMarketData(BaseModel):
    # Not unique: a bond may trade on several boards.
    SECID: str = Field(min_length=1)
    # None when there are no quotes (e.g. outside trading hours).
    BID: float | None = Field(gt=0)
    # Always null in live data.
    BIDDEPTH: None
    OFFER: float | None = Field(gt=0)
    # Always null in live data.
    OFFERDEPTH: None
    # No bounds: quotes may cross during auctions. ISS sends 0 rather than null
    # for this and the other non-nullable numeric fields below when there is no
    # data, even for bonds that did not trade.
    SPREAD: float
    BIDDEPTHT: int = Field(ge=0)
    OFFERDEPTHT: int = Field(ge=0)
    # None when the bond has not traded today.
    OPEN: float | None = Field(gt=0)
    LOW: float | None = Field(gt=0)
    HIGH: float | None = Field(gt=0)
    LAST: float | None = Field(gt=0)
    LASTCHANGE: float
    LASTCHANGEPRCNT: float
    QTY: int = Field(ge=0)
    # None on boards without regular trading stats (e.g. TQOD).
    VALUE: float | None = Field(ge=0)
    # No bounds: ranges from -100 to five-figure values for distressed bonds.
    YIELD: float | None
    VALUE_USD: float | None = Field(ge=0)
    WAPRICE: float | None = Field(gt=0)
    LASTCNGTOLASTWAPRICE: float
    WAPTOPREVWAPRICEPRCNT: float
    WAPTOPREVWAPRICE: float
    YIELDATWAPRICE: float | None
    YIELDTOPREVYIELD: float
    CLOSEYIELD: float
    CLOSEPRICE: float | None = Field(gt=0)
    MARKETPRICETODAY: float | None = Field(gt=0)
    MARKETPRICE: float | None = Field(gt=0)
    LASTTOPREVPRICE: float
    NUMTRADES: int | None = Field(ge=0)
    VOLTODAY: int | None = Field(ge=0)
    VALTODAY: int | None = Field(ge=0)
    VALTODAY_USD: int | None = Field(ge=0)
    BOARDID: str = Field(pattern=r"^[A-Z0-9]{4}$")
    # Open set of one-letter codes (N, T, B, C seen so far).
    TRADINGSTATUS: str = Field(pattern=r"^[A-Z]$")
    UPDATETIME: time
    # In days; 0 when not computed.
    DURATION: int = Field(ge=0)
    # Always null in live data.
    NUMBIDS: None
    NUMOFFERS: None
    CHANGE: float | None
    TIME: time
    # Always null in live data.
    HIGHBID: None
    LOWOFFER: None
    PRICEMINUSPREVWAPRICE: float | None
    # Always null in live data.
    LASTBID: None
    LASTOFFER: None
    LCURRENTPRICE: float | None = Field(gt=0)
    LCLOSEPRICE: float | None = Field(gt=0)
    MARKETPRICE2: float | None = Field(gt=0)
    OPENPERIODPRICE: float | None = Field(gt=0)
    SEQNUM: int = Field(gt=0)
    SYSTIME: datetime
    VALTODAY_RUR: int | None = Field(ge=0)
    # Implied rates, set only for floaters and linkers; no bounds.
    IRICPICLOSE: float | None
    BEICLOSE: float | None
    CBRCLOSE: float | None
    YIELDTOOFFER: float | None
    YIELDLASTCOUPON: float | None
    TRADINGSESSION: str | None = Field(min_length=1)
    CALLOPTIONYIELD: float | None
    CALLOPTIONDURATION: float | None = Field(ge=0)
    ZSPREAD: float | None
    ZSPREADATWAPRICE: float | None


async def get_moex_bonds_market_data(
    *, client: httpx.AsyncClient | None = None
) -> list[MoexBondMarketData]:
    rows = await moex_fetch(
        "engines/stock/markets/bonds/securities.json", "marketdata", client=client
    )
    return [MoexBondMarketData.model_validate(row) for row in rows]
