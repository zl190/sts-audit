"""
Online Bookstore Order System — Z-level version v2 - Observers & UI Layer
All print() calls live exclusively in this module.
"""

from __future__ import annotations

import uuid

from service import (
    JsonFileRepository,
    OrderObserver,
    OrderService,
)


# ╔══════════════════════════════════════════════════════════════╗
# ║  Observer Implementations (Notifications)                   ║
# ╚══════════════════════════════════════════════════════════════╝

class EmailNotifier(OrderObserver):
    def on_order_created(self, order: dict) -> None:
        print(f"\n[Email] Sent to {order['customer_email']}")
        print(f"  Dear {order['customer_name']}, "
              f"your order #{order['order_id']} has been confirmed!")
        print(f"  Amount due: ${order['final_total']}")


class SmsNotifier(OrderObserver):
    def on_order_created(self, order: dict) -> None:
        print(f"\n[SMS] Sent to {order['customer_name']}")
        print(f"  Order #{order['order_id']} confirmed, "
              f"amount ${order['final_total']}")


class InventoryNotifier(OrderObserver):
    def on_order_created(self, order: dict) -> None:
        print(f"\n[Inventory] Internal system")
        for item in order["items"]:
            print(f"  \"{item['title']}\" -- ship {item['qty']} copies")


class ActivationCodeNotifier(OrderObserver):
    """Scan order for ebooks priced > 100, generate activation codes, and email them."""

    def on_order_created(self, order: dict) -> None:
        ebook_items = [
            it for it in order["items"]
            if it["category"] == "ebook" and it["price"] > 100
        ]
        if not ebook_items:
            return

        print(f"\n[Activation Email] Sent to {order['customer_email']}")
        for item in ebook_items:
            codes = [uuid.uuid4().hex[:16].upper() for _ in range(item["qty"])]
            print(f"  \"{item['title']}\" x{item['qty']} activation codes:")
            for code in codes:
                print(f"    - {code}")


# ╔══════════════════════════════════════════════════════════════╗
# ║  UI Layer — Receipt Rendering                               ║
# ╚══════════════════════════════════════════════════════════════╝

class ReceiptView:
    """Pure display, contains no business logic."""

    @staticmethod
    def render(order: dict) -> None:
        w = 60
        print("\n" + "=" * w)
        print("            Online Bookstore - Order Receipt")
        print("=" * w)
        print(f"  Order No. : #{order['order_id']}")
        print(f"  Customer  : {order['customer_name']}")
        print(f"  Email     : {order['customer_email']}")
        print(f"  Time      : {order['created_at']}")
        print("-" * w)
        print(f"  {'Title':<20} {'Category':<10} {'Price':>6} {'Qty':>4} {'Disc.':>6} {'Subtotal':>8}")
        print("-" * w)
        for it in order["items"]:
            print(f"  {it['title']:<20} {it['category']:<10} "
                  f"{it['price']:>6.2f} {it['qty']:>4} "
                  f"{it['discount']:>6} {it['subtotal']:>8.2f}")
        print("-" * w)
        print(f"  {'Subtotal':>44}  ${order['raw_total']:>8.2f}")
        print(f"  {'Order Discount':>44}   {order['extra_discount']:>7}")
        print(f"  {'Amount Due':>44}  ${order['final_total']:>8.2f}")
        print("=" * w)


# ╔══════════════════════════════════════════════════════════════╗
# ║  Assembly (Composition Root)                                ║
# ╚══════════════════════════════════════════════════════════════╝

def build_service() -> OrderService:
    """Wire up dependencies at application startup."""
    repo = JsonFileRepository()
    service = OrderService(repo)
    service.add_observer(EmailNotifier())
    service.add_observer(SmsNotifier())
    service.add_observer(InventoryNotifier())
    service.add_observer(ActivationCodeNotifier())
    return service


# ===================== Demo =====================
if __name__ == "__main__":
    service = build_service()
    view = ReceiptView()

    order = service.create_order(
        customer_name="Alice",
        customer_email="alice@example.com",
        items=[
            {"title": "The Three-Body Problem", "category": "fiction",   "price": 45.00, "qty": 3},
            {"title": "Advanced Mathematics",   "category": "textbook",  "price": 68.00, "qty": 6},
            {"title": "The Little Prince",      "category": "children",  "price": 25.00, "qty": 2},
            {"title": "One Piece Vol.100",      "category": "comic",     "price": 15.00, "qty": 4},
            {"title": "Advanced Python (ebook)", "category": "ebook", "price": 128.00, "qty": 2},
        ],
    )
    view.render(order)
