import pytest

from moex import get_moex_daily_table

pytestmark = pytest.mark.e2e


async def test_response_matches_schema():
    assert await get_moex_daily_table()
