from moex import get_moex_resource


def test_builds_url_with_given_path_block_and_params():
    url = get_moex_resource(
        "engines/stock", "marketdata", {"ticker": "SBER", "quantity": 100}
    )
    assert url.scheme == "https"
    assert url.host == "iss.moex.com"
    assert url.path == "/iss/engines/stock"
    assert url.params["ticker"] == "SBER"
    assert url.params["quantity"] == "100"
    assert url.params["iss.meta"] == "off"
    assert url.params["iss.only"] == "marketdata"


def test_ignores_none_parameters():
    url = get_moex_resource(
        "engines/stock", "marketdata", {"ticker": None, "active": "true"}
    )
    assert "ticker" not in url.params
    assert url.params["active"] == "true"


def test_works_with_no_params_provided():
    url = get_moex_resource("engines/bonds", "marketdata")
    assert url.query == b"iss.meta=off&iss.only=marketdata"


def test_strips_leading_slash_from_path():
    url = get_moex_resource("/securities.json", "securities")
    assert url.path == "/iss/securities.json"
