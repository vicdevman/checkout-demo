from decimal import Decimal

import pytest

from checkout.cart import Cart, LineItem


def test_subtotal_adds_line_totals():
    cart = Cart()
    cart.add("MUG-BLK", "19.99", quantity=2)
    cart.add("STICKER", "5.50")
    assert cart.subtotal == Decimal("45.48")
    assert cart.item_count == 3


def test_adding_same_sku_merges_quantity():
    cart = Cart()
    cart.add("MUG-BLK", "19.99")
    cart.add("MUG-BLK", "19.99", quantity=2)
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 3


def test_empty_cart_subtotal_is_zero():
    assert Cart().subtotal == Decimal("0.00")


def test_quantity_must_be_positive():
    with pytest.raises(ValueError):
        LineItem("MUG-BLK", "19.99", quantity=0)
