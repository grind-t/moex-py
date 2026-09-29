import pytest

from moex import get_moex_bond_amortizations

pytestmark = pytest.mark.e2e


@pytest.mark.parametrize(
    "secid",
    [
        "SU26229RMFS3",  # OFZ, single payment at maturity
        "RU000A0JWSQ7",  # amortizing municipal bond
        "RU000A105A95",  # USD-denominated bond
    ],
)
async def test_response_matches_schema(secid):
    assert await get_moex_bond_amortizations(secid)
