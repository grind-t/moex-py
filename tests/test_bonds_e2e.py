import pytest

from moex import get_moex_bonds

pytestmark = pytest.mark.e2e


@pytest.mark.parametrize("primary_board", [None, 1])
async def test_response_matches_schema(primary_board):
    assert await get_moex_bonds(primary_board=primary_board)
