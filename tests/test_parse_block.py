from moex import parse_moex_block


def test_parses_a_valid_block():
    block = {"columns": ["a", "b"], "data": [[1, "one"], [2, "two"]]}
    assert parse_moex_block(block) == [{"a": 1, "b": "one"}, {"a": 2, "b": "two"}]


def test_handles_empty_data():
    assert parse_moex_block({"columns": ["a", "b"], "data": []}) == []


def test_maps_row_values_when_some_values_are_missing():
    result = parse_moex_block({"columns": ["a", "b"], "data": [[10]]})
    assert result[0]["a"] == 10
    assert result[0]["b"] is None
