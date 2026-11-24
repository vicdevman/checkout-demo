from decimal import Decimal

from checkout.money import format_money, to_money


def test_rounds_half_cents_up():
    assert to_money("2.675") == Decimal("2.68")


def test_float_input_rounds_like_the_written_amount():
    # 2.675 as a float is really 2.67499999..., but customers typed 2.675.
    assert to_money(2.675) == Decimal("2.68")


def test_format_money():
    assert format_money(1234.5) == "USD 1,234.50"
