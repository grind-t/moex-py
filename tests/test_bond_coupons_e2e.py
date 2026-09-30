from datetime import date, timedelta

import pytest

from moex import get_moex_bond_coupons

pytestmark = pytest.mark.e2e

today = date.today()


@pytest.mark.parametrize(
    "params",
    [
        {},  # oldest coupons, from the 1990s
        {  # upcoming coupons, incl. ones with unknown value
            "from_": today.isoformat(),
            "till": (today + timedelta(days=5 * 365)).isoformat(),
        },
    ],
)
async def test_response_matches_schema(params):
    assert await get_moex_bond_coupons(**params)
