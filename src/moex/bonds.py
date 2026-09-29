from typing import Literal, TypedDict

import httpx

from .core.fetch import moex_fetch


class MoexBond(TypedDict):
    SECID: str
    BOARDID: str
    SHORTNAME: str
    PREVWAPRICE: float
    YIELDATPREVWAPRICE: float
    COUPONVALUE: float
    NEXTCOUPON: str
    ACCRUEDINT: float
    PREVPRICE: float
    LOTSIZE: int
    FACEVALUE: float
    BOARDNAME: str
    STATUS: str
    MATDATE: str
    DECIMALS: int
    COUPONPERIOD: int
    ISSUESIZE: int
    PREVLEGALCLOSEPRICE: float
    PREVDATE: str
    SECNAME: str
    REMARKS: str
    MARKETCODE: str
    INSTRID: str
    SECTORID: str
    MINSTEP: float
    FACEUNIT: str
    BUYBACKPRICE: float
    BUYBACKDATE: str
    ISIN: str
    LATNAME: str
    REGNUMBER: str
    CURRENCYID: str
    ISSUESIZEPLACED: int
    LISTLEVEL: int
    SECTYPE: str
    COUPONPERCENT: float
    OFFERDATE: str
    SETTLEDATE: str
    LOTVALUE: float
    FACEVALUEONSETTLEDATE: float
    CALLOPTIONDATE: str
    PUTOPTIONDATE: str
    DATEYIELDFROMISSUER: str


async def get_moex_bonds(
    *,
    primary_board: Literal[1, 0] | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[MoexBond]:
    return await moex_fetch(
        "engines/stock/markets/bonds/securities.json",
        "securities",
        {"primary_board": primary_board},
        client,
    )
