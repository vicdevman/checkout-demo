"""Create one branch per realistic bug, each based on a green main.

Run from the repo root after your first commit on main:
    python scripts/create_demo_branches.py
Then push them all:
    git push origin --all

Each branch is one small commit that a teammate might plausibly make,
and each one breaks at least one test in a different way.
"""

import subprocess
from pathlib import Path

BUGS = [
    {
        "branch": "refactor/order-history-pagination",
        "message": "Simplify order history pagination",
        "file": "checkout/orders.py",
        "old": "start = (page - 1) * per_page",
        "new": "start = page * per_page",
        "kind": "off-by-one: page 1 skips the newest orders",
    },
    {
        "branch": "refactor/simplify-order-total",
        "message": "Compute tax straight from the cart subtotal",
        "file": "checkout/pricing.py",
        "old": "tax_amount = tax(discounted, tax_rate)",
        "new": "tax_amount = tax(cart.subtotal, tax_rate)",
        "kind": "business logic: tax charged before the coupon discount",
    },
    {
        "branch": "chore/shipping-threshold-cleanup",
        "message": "Tidy free shipping check",
        "file": "checkout/pricing.py",
        "old": "if discounted_subtotal >= FREE_SHIPPING_THRESHOLD:",
        "new": "if discounted_subtotal > FREE_SHIPPING_THRESHOLD:",
        "kind": "boundary: an order of exactly $50.00 is charged shipping",
    },
    {
        "branch": "perf/skip-string-conversion",
        "message": "Avoid string conversion when building amounts",
        "file": "checkout/money.py",
        "old": "Decimal(str(value))",
        "new": "Decimal(value)",
        "kind": "precision: float inputs round to the wrong cent",
    },
    {
        "branch": "refactor/rename-coupon-helper",
        "message": "Rename apply_coupon to apply_discount",
        "file": "checkout/pricing.py",
        "old": "def apply_coupon(subtotal, code=None):",
        "new": "def apply_discount(subtotal, code=None):",
        "kind": "broken rename: callers and tests still use the old name",
    },
]


def git(*args):
    subprocess.run(["git", *args], check=True)


def main():
    for bug in BUGS:
        git("checkout", "--quiet", "-B", bug["branch"], "main")
        path = Path(bug["file"])
        text = path.read_text(encoding="utf-8")
        assert text.count(bug["old"]) == 1, f"{bug['old']!r} not found once in {path}"
        path.write_text(text.replace(bug["old"], bug["new"]), encoding="utf-8")
        git("commit", "--quiet", "-am", bug["message"])
        print(f"created {bug['branch']:<38} {bug['kind']}")
    git("checkout", "--quiet", "main")


if __name__ == "__main__":
    main()
