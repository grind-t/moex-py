from typing import TypedDict

import httpx

from .core.fetch import moex_fetch


class MoexDailyTableRow(TypedDict):
    date: str
    is_work_day: int
    start_time: str
    stop_time: str


async def get_moex_daily_table(
    *, client: httpx.AsyncClient | None = None
) -> list[MoexDailyTableRow]:
    return await moex_fetch("engines/stock.json", "dailytable", client=client)
