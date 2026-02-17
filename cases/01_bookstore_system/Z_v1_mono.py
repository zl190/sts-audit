"""
Online Bookstore Order System — Z-level version (decoupled)
- Strategy pattern  — discount calculation
- Observer pattern  — order notifications
- UI fully separated from business logic
"""

from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from datetime import datetime


# ╔══════════════════════════════════════════════════════════════╗
# ║  1. Strategy Pattern — Discount Calculation                 ║
# ╚══════════════════════════════════════════════════════════════╝

class DiscountStrategy(ABC):
    """Abstract base class for discount strategies."""

    @abstractmethod
    def calculate(self, price: float, qty: int) -> float:
        """Return the discount ratio (0.0 – 1.0)."""


class FictionDiscount(DiscountStrategy):
    def calculate(self, price: float, qty: int) -> float:
        if qty >= 5:
            return 0.20
        if qty >= 3:
            return 0.15
        return 0.10


class TextbookDiscount(DiscountStrategy):
    def calculate(self, price: float, qty: int) -> float:
        if qty >= 10:
            return 0.25
        if qty >= 5:
            return 0.15
        return 0.05


class ChildrenDiscount(DiscountStrategy):
    def calculate(self, price: float, qty: int) -> float:
        if qty >= 5:
            return 0.30
        if qty >= 3:
            return 0.20
        return 0.15


class ComicDiscount(DiscountStrategy):
    def calculate(self, price: float, qty: int) -> float:
        if qty >= 10:
            return 0.20
        if qty >= 3:
            return 0.10
        return 0.05


class NoDiscount(DiscountStrategy):
    def calculate(self, price: float, qty: int) -> float:
        return 0.0


class DiscountStrategyFactory:
    """Return the appropriate strategy instance for a book category."""

    _strategies: dict[str, DiscountStrategy] = {
        "fiction":   FictionDiscount(),
        "textbook":  TextbookDiscount(),
        "children":  ChildrenDiscount(),
        "comic":     ComicDiscount(),
    }
    _default = NoDiscount()

    @classmethod
    def get(cls, category: str) -> DiscountStrategy:
        return cls._strategies.get(category, cls._default)


class OrderDiscountCalculator:
    """Order-level threshold discount, independently replaceable."""

    @staticmethod
    def calculate(total: float) -> float:
        if total >= 500:
            return 0.05
        if total >= 300:
            return 0.03
        return 0.0


# ╔══════════════════════════════════════════════════════════════╗
# ║  2. Observer Pattern — Order Notifications                  ║
# ╚══════════════════════════════════════════════════════════════╝

class OrderObserver(ABC):
    """Observer for order events."""

    @abstractmethod
    def on_order_created(self, order: dict) -> None: ...


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


# ╔══════════════════════════════════════════════════════════════╗
# ║  3. Data Persistence Layer (Repository)                     ║
# ╚══════════════════════════════════════════════════════════════╝

class OrderRepository(ABC):
    @abstractmethod
    def load_all(self) -> list[dict]: ...

    @abstractmethod
    def save(self, orders: list[dict]) -> None: ...

    @abstractmethod
    def next_id(self) -> int: ...


class JsonFileRepository(OrderRepository):
    def __init__(self, path: str = "orders_z.json"):
        self._path = path
        self._orders: list[dict] = self.load_all()

    def load_all(self) -> list[dict]:
        if os.path.exists(self._path):
            with open(self._path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save(self, orders: list[dict]) -> None:
        self._orders = orders
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)

    def next_id(self) -> int:
        return len(self._orders) + 1


# ╔══════════════════════════════════════════════════════════════╗
# ║  4. Core Business — OrderService (pure logic, no UI)        ║
# ╚══════════════════════════════════════════════════════════════╝

class OrderService:
    def __init__(self, repo: OrderRepository):
        self._repo = repo
        self._observers: list[OrderObserver] = []

    # -- Observer management --
    def add_observer(self, observer: OrderObserver) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer: OrderObserver) -> None:
        self._observers.remove(observer)

    def _notify(self, order: dict) -> None:
        for obs in self._observers:
            obs.on_order_created(order)

    # -- Business method --
    def create_order(self, customer_name: str, customer_email: str,
                     items: list[dict]) -> dict:
        # Calculate per-item discount
        total = 0.0
        detail_lines = []

        for item in items:
            strategy = DiscountStrategyFactory.get(item["category"])
            discount = strategy.calculate(item["price"], item["qty"])
            subtotal = item["price"] * item["qty"] * (1 - discount)
            total += subtotal
            detail_lines.append({
                "title":    item["title"],
                "category": item["category"],
                "price":    item["price"],
                "qty":      item["qty"],
                "discount": f"{discount:.0%}",
                "subtotal": round(subtotal, 2),
            })

        # Order-level threshold discount
        extra_discount = OrderDiscountCalculator.calculate(total)
        final_total = round(total * (1 - extra_discount), 2)

        # Build order
        order = {
            "order_id":       self._repo.next_id(),
            "customer_name":  customer_name,
            "customer_email": customer_email,
            "items":          detail_lines,
            "raw_total":      round(total, 2),
            "extra_discount": f"{extra_discount:.0%}",
            "final_total":    final_total,
            "created_at":     datetime.now().isoformat(),
        }

        # Persist
        orders = self._repo.load_all()
        orders.append(order)
        self._repo.save(orders)

        # Notify all observers
        self._notify(order)

        return order


# ╔══════════════════════════════════════════════════════════════╗
# ║  5. UI Layer — Fully Separated from Business Logic          ║
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
# ║  6. Assembly (Composition Root)                             ║
# ╚══════════════════════════════════════════════════════════════╝

def build_service() -> OrderService:
    """Wire up dependencies at application startup."""
    repo = JsonFileRepository()
    service = OrderService(repo)
    service.add_observer(EmailNotifier())
    service.add_observer(SmsNotifier())
    service.add_observer(InventoryNotifier())
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
        ],
    )
    view.render(order)
