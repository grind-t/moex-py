import pytest

from moex import get_moex_securities

pytestmark = pytest.mark.e2e


@pytest.mark.parametrize(
    "params",
    [
        {},  # indices, futures and funds without an issuer
        {"q": "ОФЗ"},  # state bonds with a registration number
        {"engine": "stock", "market": "shares"},  # shares with an issuer
    ],
)
async def test_response_matches_schema(params):
    assert await get_moex_securities(**params)
