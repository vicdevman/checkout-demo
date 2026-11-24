"""Money helpers. All amounts are Decimal, rounded to whole cents."""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_money(value):
    """Convert a number or string to a Decimal amount in whole cents."""
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def format_money(amount, currency="USD"):
    """Format an amount for display, e.g. 'USD 12.50'."""
    return f"{currency} {to_money(amount):,.2f}"
