import httpx

from .securities import MoexSecurity, get_moex_securities


async def get_moex_bond_securities(
    *, client: httpx.AsyncClient | None = None
) -> list[MoexSecurity]:
    if client is None:
        async with httpx.AsyncClient() as own_client:
            return await get_moex_bond_securities(client=own_client)

    securities: list[MoexSecurity] = []
    start = 0

    while True:
        chunk = await get_moex_securities(
            engine="stock",
            market="bonds",
            is_trading=1,
            start=start,
            limit=100,
            client=client,
        )

        securities.extend(chunk)
        start += len(chunk)

        if len(chunk) < 100:
            return securities
