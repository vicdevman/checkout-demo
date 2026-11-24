"""Order pricing: coupons, shipping and tax.

Order of operations matters: discount the subtotal first, then add shipping,
then charge tax on the discounted goods only (shipping is not taxed).
"""

from decimal import Decimal

from checkout.money import to_money

FREE_SHIPPING_THRESHOLD = Decimal("50.00")
FLAT_SHIPPING = Decimal("4.99")

COUPONS = {
    "WELCOME10": {"type": "percent", "value": Decimal("10")},
    "SAVE5": {"type": "fixed", "value": Decimal("5.00")},
}


def apply_coupon(subtotal, code=None):
    """Return the subtotal after the coupon. Unknown codes raise ValueError."""
    if not code:
        return to_money(subtotal)
    coupon = COUPONS.get(code.upper())
    if coupon is None:
        raise ValueError(f"unknown coupon: {code}")
    if coupon["type"] == "percent":
        discounted = subtotal * (1 - coupon["value"] / 100)
    else:
        discounted = subtotal - coupon["value"]
    return to_money(max(discounted, Decimal("0")))


def shipping_cost(discounted_subtotal):
    """Orders at or above the threshold ship free."""
    if discounted_subtotal >= FREE_SHIPPING_THRESHOLD:
        return Decimal("0.00")
    return FLAT_SHIPPING


def tax(amount, rate):
    """Tax on an amount, where rate is a percentage like 8.25."""
    return to_money(amount * Decimal(str(rate)) / 100)


def order_total(cart, tax_rate, coupon=None):
    """Price a cart and return each part of the total."""
    discounted = apply_coupon(cart.subtotal, coupon)
    shipping = shipping_cost(discounted)
    tax_amount = tax(discounted, tax_rate)
    return {
        "subtotal": cart.subtotal,
        "discounted": discounted,
        "shipping": shipping,
        "tax": tax_amount,
        "total": to_money(discounted + shipping + tax_amount),
    }
