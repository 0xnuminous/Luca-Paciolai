from luca_paciolai.llm import parse_transaction


def test_parse_transaction_amount() -> None:
    result = parse_transaction("I bought 2 coffees for 10 dollars", [])
    assert result["amount"] == 10.0
