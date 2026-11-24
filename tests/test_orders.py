import pytest

from checkout.orders import page_count, paginate

ORDERS = [{"id": f"ORD-{n:03d}", "placed_at": n} for n in range(1, 26)]  # 25 orders


def ids(orders):
    return [order["id"] for order in orders]


def test_first_page_shows_newest_orders():
    assert ids(paginate(ORDERS, page=1)) == [f"ORD-{n:03d}" for n in range(25, 15, -1)]


def test_last_page_is_partial():
    assert ids(paginate(ORDERS, page=3)) == [f"ORD-{n:03d}" for n in range(5, 0, -1)]


def test_page_past_the_end_is_empty():
    assert paginate(ORDERS, page=4) == []


def test_invalid_page_is_rejected():
    with pytest.raises(ValueError):
        paginate(ORDERS, page=0)


def test_page_count_rounds_up():
    assert page_count(ORDERS) == 3
    assert page_count([]) == 1
