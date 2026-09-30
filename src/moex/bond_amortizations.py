from datetime import date
from typing import Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field

from .core.fetch import moex_fetch


class MoexBondAmortization(BaseModel):
    isin: str = Field(pattern=r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$")
    name: str = Field(min_length=1)
    # Not always whole: e.g. gold-linked bonds have a fractional issue volume.
    issuevalue: float = Field(gt=0)
    amortdate: date = Field(strict=False)
    facevalue: float = Field(gt=0)
    initialfacevalue: float = Field(gt=0)
    faceunit: str = Field(pattern=r"^[A-Z]{3}$")
    # May exceed 100 for indexed bonds; 0 for future payments not yet known.
    valueprc: float = Field(ge=0)
    value: float = Field(ge=0)
    # None when the payment amount is not known yet.
    value_rub: float | None = Field(gt=0)
    data_source: Literal["amortization", "maturity"]
    secid: str = Field(min_length=1)
    primary_boardid: str = Field(pattern=r"^[A-Z0-9]{4}$")


async def get_moex_bond_amortizations(
    id: str,
    *,
    lang: Literal["ru", "en"] | None = None,
    from_: str | None = None,
    till: str | None = None,
    limit: int | None = None,
    start: int | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[MoexBondAmortization]:
    rows = await moex_fetch(
        f"securities/{id}/bondization.json",
        "amortizations",
        {
            "lang": lang,
            "from": from_,
            "till": till,
            "limit": "unlimited" if limit is None else limit,
            "start": start,
        },
        client,
    )
    return [MoexBondAmortization.model_validate(row) for row in rows]
