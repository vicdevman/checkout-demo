"""Order history for the account page."""

import math


def paginate(orders, page, per_page=10):
    """Return one 1-indexed page of orders, newest first."""
    if page < 1:
        raise ValueError("page must be 1 or greater")
    if per_page < 1:
        raise ValueError("per_page must be 1 or greater")
    newest_first = sorted(orders, key=lambda order: order["placed_at"], reverse=True)
    start = (page - 1) * per_page
    return newest_first[start : start + per_page]


def page_count(orders, per_page=10):
    """How many pages the account page needs to show every order."""
    return max(1, math.ceil(len(orders) / per_page))
