# Imported as a module: the `date` field would otherwise shadow the type.
import datetime as dt

import httpx
from pydantic import BaseModel

from .core.fetch import moex_fetch


# Exceptions to the regular calendar: weekday holidays and working weekends.
class MoexDailyTableRow(BaseModel):
    date: dt.date
    is_work_day: bool
    # None (or 00:00:00 for both) on some non-working days, so start < stop
    # does not always hold.
    start_time: dt.time | None
    stop_time: dt.time | None


async def get_moex_daily_table(
    *, client: httpx.AsyncClient | None = None
) -> list[MoexDailyTableRow]:
    rows = await moex_fetch("engines/stock.json", "dailytable", client=client)
    return [MoexDailyTableRow.model_validate(row) for row in rows]
