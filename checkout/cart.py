"""Shopping cart: line items and subtotal."""

from dataclasses import dataclass, field

from checkout.money import to_money


@dataclass
class LineItem:
    sku: str
    unit_price: object
    quantity: int = 1

    def __post_init__(self):
        if self.quantity < 1:
            raise ValueError("quantity must be at least 1")
        self.unit_price = to_money(self.unit_price)

    @property
    def total(self):
        return to_money(self.unit_price * self.quantity)


@dataclass
class Cart:
    items: list = field(default_factory=list)

    def add(self, sku, unit_price, quantity=1):
        for item in self.items:
            if item.sku == sku:
                item.quantity += quantity
                return item
        item = LineItem(sku, unit_price, quantity)
        self.items.append(item)
        return item

    @property
    def subtotal(self):
        return to_money(sum((item.total for item in self.items), start=0))

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items)
