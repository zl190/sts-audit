"""
Online Bookstore Order System — Z-level version v2 - Service Layer
Pure business logic, zero UI dependencies. Observers and ReceiptView live in views.py.
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


class EbookDiscount(DiscountStrategy):
    def calculate(self, price: float, qty: int) -> float:
        if price > 100:
            return 0.05
        return 0.0


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
        "ebook":     EbookDiscount(),
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
# ║  2. Observer Abstract Contract                              ║
# ╚══════════════════════════════════════════════════════════════╝

class OrderObserver(ABC):
    """Observer for order events."""

    @abstractmethod
    def on_order_created(self, order: dict) -> None: ...


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

    def add_observer(self, observer: OrderObserver) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer: OrderObserver) -> None:
        self._observers.remove(observer)

    def _notify(self, order: dict) -> None:
        for obs in self._observers:
            obs.on_order_created(order)

    def create_order(self, customer_name: str, customer_email: str,
                     items: list[dict]) -> dict:
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

        extra_discount = OrderDiscountCalculator.calculate(total)
        final_total = round(total * (1 - extra_discount), 2)

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

        orders = self._repo.load_all()
        orders.append(order)
        self._repo.save(orders)

        self._notify(order)
        return order
