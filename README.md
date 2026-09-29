# grind-t-moex

Async Python client for the [Moscow Exchange ISS API](https://iss.moex.com/iss/reference/).
Python port of [`@grind-t/moex`](https://github.com/grind-t/moex).

## Installation

```sh
uv add grind-t-moex
```

## Usage

```python
import asyncio

import httpx
import moex


async def main():
    bonds = await moex.get_moex_bonds(primary_board=1)
    print(bonds[0]["SECID"], bonds[0]["COUPONPERCENT"])

    # Reuse one connection pool for several requests
    async with httpx.AsyncClient() as client:
        description = await moex.get_moex_security_description("SU26238RMFS4", client=client)
        amortizations = await moex.get_moex_bond_amortizations("SU26238RMFS4", client=client)


asyncio.run(main())
```

## Functions

| Function | ISS resource |
| --- | --- |
| `get_moex_bonds(primary_board=)` | `engines/stock/markets/bonds/securities` → `securities` |
| `get_moex_bonds_market_data()` | `engines/stock/markets/bonds/securities` → `marketdata` |
| `get_moex_bonds_market_yield()` | `engines/stock/markets/bonds/securities` → `marketdata_yields` |
| `get_moex_bond_coupons(...)` | `statistics/engines/stock/markets/bonds/bondization` → `coupons` |
| `get_moex_bond_amortizations(id, ...)` | `securities/{id}/bondization` → `amortizations` |
| `get_moex_bond_securities()` | all traded bonds from `securities`, paginated |
| `get_moex_securities(...)` | `securities` → `securities` |
| `get_moex_security_description(id)` | `securities/{id}` → `description` |
| `get_moex_daily_table()` | `engines/stock` → `dailytable` |

Low-level helpers: `moex_fetch(path, block, params)`, `get_moex_resource`, `parse_moex_block`.

All functions accept an optional `client: httpx.AsyncClient`. The `from` query
parameter is passed as `from_`.
