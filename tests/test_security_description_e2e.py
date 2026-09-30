import pytest

from moex import get_moex_security_description

pytestmark = pytest.mark.e2e


@pytest.mark.parametrize("secid", ["SBER", "SU26238RMFS4", "IMOEX", "USD000UTSTOM"])
async def test_response_matches_schema(secid):
    description = await get_moex_security_description(secid)
    assert description.SECID == secid
