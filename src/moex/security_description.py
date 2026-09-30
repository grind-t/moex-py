from datetime import date, time
from typing import Literal

import httpx
from pydantic import BaseModel, Field

from .core.fetch import moex_get_json


# Keys vary by security type; only TYPE, TYPENAME, GROUP and GROUPNAME are
# present for every security. Absent keys are None.
class MoexSecurityDescription(BaseModel):
    # Absent for currency fixings and OTC currency indices.
    SECID: str | None = Field(default=None, min_length=1)
    # Absent for old commodity futures and some indices.
    SHORTNAME: str | None = Field(default=None, min_length=1)
    NAME: str | None = Field(default=None, min_length=1)
    LATSHORTNAME: str | None = Field(default=None, min_length=1)
    LATNAME: str | None = Field(default=None, min_length=1)
    CALCMODE: str | None = Field(default=None, pattern=r"^[A-Z0-9-]+$")
    CALCMODEDESCR: str | None = Field(default=None, min_length=1)
    CURRENCYID: str | None = Field(default=None, pattern=r"^[A-Z]{3}$")
    FREQUENCY: str | None = Field(default=None, min_length=1)
    SCHEDULE: str | None = Field(default=None, min_length=1)
    DECIMALS: int | None = Field(default=None, ge=0)
    INITIALVALUE: float | None = Field(default=None, gt=0)
    ISSUEDATE: date | None = None
    TRADINGSESSION: str | None = Field(default=None, min_length=1)
    # iNAV indices mark the fund with a leading or trailing underscore.
    UNDERLYINGTICKER: str | None = Field(default=None, pattern=r"^_?[A-Z0-9]+_?$")
    UNDERLYINGISIN: str | None = Field(
        default=None, pattern=r"^_?[A-Z]{2}[A-Z0-9]{9}[0-9]_?$"
    )
    REBALANCE: str | None = Field(default=None, min_length=1)
    WEIGHTLIMITTYPE: str | None = Field(default=None, min_length=1)
    TYPENAME: str = Field(min_length=1)
    GROUP: str = Field(pattern=r"^[a-z_]+$")
    TYPE: str = Field(pattern=r"^[a-z_]+$")
    GROUPNAME: str = Field(min_length=1)
    FIRSTCALCDATE: date | None = None
    # A count, but "переменное" (variable) for some indices.
    CONSTITUENTS: str | None = Field(default=None, min_length=1)
    DESCRIPTION: str | None = Field(default=None, min_length=1)
    INITIALCAPITALIZATION: float | None = Field(default=None, gt=0)
    INITIALD: float | None = Field(default=None, gt=0)
    ISSUENAME: str | None = Field(default=None, min_length=1)
    # One index has a truncated 11-character ISIN (check digit missing).
    ISIN: str | None = Field(default=None, pattern=r"^[A-Z]{2}[A-Z0-9]{9}[0-9]?$")
    # Not always whole: down to 1e-05 for some shares.
    FACEVALUE: float | None = Field(default=None, gt=0)
    # Includes non-ISO codes such as SUR, GLD and BKT.
    FACEUNIT: str | None = Field(default=None, pattern=r"^[A-Z]{3}$")
    HASPROSPECTUS: bool | None = None
    HASDEFAULT: bool | None = None
    HASTECHNICALDEFAULT: bool | None = None
    # A 0/1 flag, though ISS declares it a number.
    EMITENTMISMATCHCUR: int | None = Field(default=None, ge=0, le=1)
    ISQUALIFIEDINVESTORS: bool | None = None
    QUALINVESTORGROUP: str | None = Field(default=None, min_length=1)
    EMITTER_ID: int | None = Field(default=None, gt=0)
    REGNUMBER: str | None = Field(default=None, min_length=1)
    ISSUESIZE: int | None = Field(default=None, gt=0)
    REGISTRY_DATE: date | None = None
    DECISIONDATE: date | None = None
    LISTLEVEL: int | None = Field(default=None, ge=1, le=3)
    MORNINGSESSION: bool | None = None
    EVENINGSESSION: bool | None = None
    WEEKENDSESSION: bool | None = None
    MATDATE: date | None = None
    INITIALFACEVALUE: float | None = Field(default=None, gt=0)
    STARTDATEMOEX: date | None = None
    ISCONCESSIONAGREEMENT: bool | None = None
    INCLUDEDBYMOEX: bool | None = None
    DAYSTOREDEMPTION: int | None = Field(default=None, ge=0)
    COUPONFREQUENCY: int | None = Field(default=None, gt=0)
    COUPONDATE: date | None = None
    # 0 for some structured bonds.
    COUPONPERCENT: float | None = Field(default=None, ge=0)
    COUPONVALUE: float | None = Field(default=None, ge=0)
    BOND_TYPE: str | None = Field(default=None, min_length=1)
    BOND_SUBTYPE: (
        Literal["До погашения", "До оферты (put)", "До оферты (call)", "Бессрочные"]
        | None
    ) = None
    EARLYREPAYMENT: bool | None = None
    COUPON_BENCHMARK: str | None = Field(default=None, pattern=r"^[A-Z]+$")
    # ISS declares it a string, e.g. "1.30".
    COUPON_BENCHMARK_SPREAD: str | None = Field(
        default=None, pattern=r"^-?[0-9]+\.[0-9]+$"
    )
    AMORTBOND: bool | None = None
    BUYBACKDATE: date | None = None
    EMITTER_VALUE_BUILDING: bool | None = None
    LOTSIZE: int | None = Field(default=None, gt=0)
    TIMETABLE: str | None = Field(default=None, min_length=1)
    DELIVERYTYPE: str | None = Field(default=None, min_length=1)
    FRSTTRADE: date | None = None
    LSTTRADE: date | None = None
    LSTDELDATE: date | None = None
    ASSETCODE: str | None = Field(default=None, pattern=r"^[A-Za-z0-9]+$")
    EXECTYPE: str | None = Field(default=None, min_length=1)
    CONTRACTNAME: str | None = Field(default=None, min_length=1)
    GROUPTYPE: str | None = Field(default=None, min_length=1)
    UNIT: str | None = Field(default=None, min_length=1)
    EXPIRATION_TYPE: str | None = Field(default=None, min_length=1)
    EXPIRATION_TIME: time | None = None
    SETTLETYPE: Literal["Расчетный", "Поставочный"] | None = None
    OPTIONTYPE: Literal["C", "P"] | None = None
    STRIKE: float | None = Field(default=None, gt=0)
    MARGINSTYLE: Literal["Премиальный", "Маржируемый"] | None = None
    UNDERLYINGASSET: str | None = Field(default=None, min_length=1)
    SERIES_NAME: str | None = Field(default=None, min_length=1)
    DEPOSITARY_ORG_NAME: str | None = Field(default=None, min_length=1)
    # Not always whole: e.g. 0.2 shares per receipt.
    SHARESPERRECEIPT: float | None = Field(default=None, gt=0)
    HIGHRISK: bool | None = None
    SECSUBTYPE: str | None = Field(default=None, min_length=1)
    SUBORDBOND: bool | None = None
    PROGRAMREGISTRYNUMBER: str | None = Field(default=None, min_length=1)
    STRUCTBOND: bool | None = None
    ASSET: str | None = Field(default=None, min_length=1)
    PARENTINDEX: str | None = Field(default=None, min_length=1)
    ISPARENT: bool | None = None
    BBG: str | None = Field(default=None, min_length=1)
    RIC: str | None = Field(default=None, min_length=1)
    VOLUME_UNIT: str | None = Field(default=None, min_length=1)
    DEPOSITARYNOTETYPE: str | None = Field(default=None, min_length=1)
    ISSUESIZEPLANNED: int | None = Field(default=None, gt=0)
    PERPETUAL_FUTURES: bool | None = None
    FOSECTYPE: str | None = Field(default=None, pattern=r"^[A-Z0-9]+$")
    # The fields below come only with old commodity futures.
    FACEUNITNAME: str | None = Field(default=None, min_length=1)
    DELIVERYMINQTY: str | None = Field(default=None, min_length=1)
    PRICEFULLNAME: str | None = Field(default=None, min_length=1)
    MINPRICEFLUCT: str | None = Field(default=None, min_length=1)
    DURATION: int | None = Field(default=None, gt=0)
    DELCOMMISSION: str | None = Field(default=None, min_length=1)
    COMMISSIONRATE: float | None = Field(default=None, gt=0)
    FINALPRICEMETHOD: str | None = Field(default=None, min_length=1)
    STARTDELDATE: date | None = None
    PRICEMVTLIMITEXTNAME: str | None = Field(default=None, min_length=1)
    SHARELIMIT: float | None = Field(default=None, gt=0, le=100)
    THRESHOLD: int | None = Field(default=None, gt=0)
    MAXORDVOL: int | None = Field(default=None, gt=0)
    DMRATEEXTNAME: str | None = Field(default=None, min_length=1)
    TIMECOURSEINT: time | None = None
    TIMECOURSECLR: time | None = None
    # Only for the bi-currency basket.
    BASKET_DESCR1: str | None = Field(default=None, min_length=1)
    BASKET_DESCR2: str | None = Field(default=None, min_length=1)
    BASKET_DESCR3: str | None = Field(default=None, min_length=1)
    BASKET_DESCR4: str | None = Field(default=None, min_length=1)
    BASKET_DESCR5: str | None = Field(default=None, min_length=1)


async def get_moex_security_description(
    id: str, *, client: httpx.AsyncClient | None = None
) -> MoexSecurityDescription:
    data = await moex_get_json(f"securities/{id}.json", "description", client=client)
    description = data["description"]
    columns = description["columns"]
    name_index = columns.index("name")
    value_index = columns.index("value")

    # Values are strings; the model converts them by field type.
    result = {row[name_index]: row[value_index] for row in description["data"]}
    return MoexSecurityDescription.model_validate(result)
