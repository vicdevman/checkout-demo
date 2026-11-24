from decimal import Decimal

import pytest

from checkout.cart import Cart
from checkout.pricing import apply_coupon, order_total, shipping_cost, tax


def test_percent_coupon():
    assert apply_coupon(Decimal("100.00"), "WELCOME10") == Decimal("90.00")


def test_coupon_codes_are_case_insensitive():
    assert apply_coupon(Decimal("100.00"), "welcome10") == Decimal("90.00")


def test_fixed_coupon_never_goes_below_zero():
    assert apply_coupon(Decimal("3.00"), "SAVE5") == Decimal("0.00")


def test_unknown_coupon_is_rejected():
    with pytest.raises(ValueError):
        apply_coupon(Decimal("10.00"), "FREESTUFF")


def test_free_shipping_starts_exactly_at_threshold():
    assert shipping_cost(Decimal("50.00")) == Decimal("0.00")


def test_flat_shipping_below_threshold():
    assert shipping_cost(Decimal("49.99")) == Decimal("4.99")


def test_tax_rounds_to_cents():
    assert tax(Decimal("19.99"), 8.25) == Decimal("1.65")


def test_tax_is_charged_on_discounted_goods():
    cart = Cart()
    cart.add("HOODIE", "30.00", quantity=2)  # 60.00
    result = order_total(cart, tax_rate=8.25, coupon="WELCOME10")
    assert result["discounted"] == Decimal("54.00")
    assert result["shipping"] == Decimal("0.00")
    assert result["tax"] == Decimal("4.46")
    assert result["total"] == Decimal("58.46")


def test_shipping_is_not_taxed():
    cart = Cart()
    cart.add("CAP", "20.00")
    result = order_total(cart, tax_rate=10)
    assert result["shipping"] == Decimal("4.99")
    assert result["tax"] == Decimal("2.00")
    assert result["total"] == Decimal("26.99")
