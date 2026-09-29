from collections.abc import Mapping

import httpx

BASE_URL = "https://iss.moex.com/iss/"

Params = Mapping[str, str | int | None]


def get_moex_resource(path: str, block: str, params: Params | None = None) -> httpx.URL:
    query = {
        key: str(value) for key, value in (params or {}).items() if value is not None
    }
    query["iss.meta"] = "off"
    query["iss.only"] = block

    return httpx.URL(BASE_URL + path.lstrip("/"), params=query)
