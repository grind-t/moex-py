from datetime import date
from typing import TypedDict

import httpx

from .core.fetch import moex_get_json


class MoexSecurityDescription(TypedDict):
    SECID: str
    SHORTNAME: str
    NAME: str
    LATSHORTNAME: str
    LATNAME: str
    CALCMODE: str
    CALCMODEDESCR: str
    CURRENCYID: str
    FREQUENCY: str
    SCHEDULE: str
    DECIMALS: int
    INITIALVALUE: float
    ISSUEDATE: date
    TRADINGSESSION: str
    UNDERLYINGTICKER: str
    UNDERLYINGISIN: str
    REBALANCE: str
    WEIGHTLIMITTYPE: str
    TYPENAME: str
    GROUP: str
    TYPE: str
    GROUPNAME: str
    FIRSTCALCDATE: date
    CONSTITUENTS: str
    DESCRIPTION: str
    INITIALCAPITALIZATION: float
    INITIALD: float
    ISSUENAME: str
    ISIN: str
    FACEVALUE: float
    FACEUNIT: str
    HASPROSPECTUS: bool
    HASDEFAULT: bool
    HASTECHNICALDEFAULT: bool
    EMITENTMISMATCHCUR: int
    ISQUALIFIEDINVESTORS: bool
    QUALINVESTORGROUP: str
    EMITTER_ID: int
    REGNUMBER: str
    ISSUESIZE: int
    REGISTRY_DATE: date
    DECISIONDATE: date
    LISTLEVEL: int
    MORNINGSESSION: bool
    EVENINGSESSION: bool
    WEEKENDSESSION: bool
    MATDATE: date
    INITIALFACEVALUE: float
    STARTDATEMOEX: date
    ISCONCESSIONAGREEMENT: bool
    INCLUDEDBYMOEX: bool
    DAYSTOREDEMPTION: int
    COUPONFREQUENCY: int
    COUPONDATE: date
    COUPONPERCENT: float
    COUPONVALUE: float
    BOND_TYPE: str
    BOND_SUBTYPE: str
    EARLYREPAYMENT: bool
    COUPON_BENCHMARK: str
    COUPON_BENCHMARK_SPREAD: str
    AMORTBOND: bool
    BUYBACKDATE: date
    EMITTER_VALUE_BUILDING: bool
    LOTSIZE: int
    TIMETABLE: str
    DELIVERYTYPE: str
    FRSTTRADE: date
    LSTTRADE: date
    LSTDELDATE: date
    ASSETCODE: str
    EXECTYPE: str
    CONTRACTNAME: str
    GROUPTYPE: str
    UNIT: str
    EXPIRATION_TYPE: str
    EXPIRATION_TIME: str
    SETTLETYPE: str
    OPTIONTYPE: str
    STRIKE: float
    MARGINSTYLE: str
    UNDERLYINGASSET: str
    SERIES_NAME: str
    DEPOSITARY_ORG_NAME: str
    SHARESPERRECEIPT: int
    HIGHRISK: bool
    SECSUBTYPE: str
    SUBORDBOND: bool
    PROGRAMREGISTRYNUMBER: str
    STRUCTBOND: bool


def _parse_value(value: str | None, type: str) -> str | float | bool | date | None:
    if value is None:
        return None
    if type == "number":
        return float(value) if any(c in value for c in ".eE") else int(value)
    if type == "boolean":
        return value == "1"
    if type == "date":
        return date.fromisoformat(value)
    return value


async def get_moex_security_description(
    id: str, *, client: httpx.AsyncClient | None = None
) -> MoexSecurityDescription:
    data = await moex_get_json(f"securities/{id}.json", "description", client=client)
    description = data["description"]
    columns = description["columns"]
    name_index = columns.index("name")
    value_index = columns.index("value")
    type_index = columns.index("type")

    result = {
        row[name_index]: _parse_value(row[value_index], row[type_index])
        for row in description["data"]
    }
    return result  # type: ignore[return-value]
