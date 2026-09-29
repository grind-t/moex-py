from typing import Any

import httpx

from .parse_block import parse_moex_block
from .resource import Params, get_moex_resource


async def moex_get_json(
    path: str,
    block: str,
    params: Params | None = None,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    url = get_moex_resource(path, block, params)

    if client is None:
        async with httpx.AsyncClient() as own_client:
            response = await own_client.get(url)
    else:
        response = await client.get(url)

    response.raise_for_status()
    return response.json()


async def moex_fetch(
    path: str,
    block: str,
    params: Params | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[Any]:
    data = await moex_get_json(path, block, params, client)
    return parse_moex_block(data[block])
