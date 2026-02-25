"""
Warehouse Inventory Management System — Z-level service layer (decoupled)
Pure business logic with no I/O (no print, no file access in core logic).
Uses Strategy pattern for pricing and Observer pattern for notifications.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Protocol


# ---- Domain Models ----

class Priority(Enum):
    NORMAL = "normal"
    URGENT = "urgent"
    BULK = "bulk"


@dataclass
class Product:
    sku: str
    name: str
    category: str
    quantity: int
    unit_cost: float
    warehouse: str = "main"
    added: str = ""

    def __post_init__(self):
        if not self.added:
            self.added = datetime.now().isoformat()


@dataclass
class OrderResult:
    status: str
    sku: str
    quantity: int = 0
    total: float = 0.0
    customer: str = ""
    shortfall: int = 0
    reason: str = ""


@dataclass
class TransactionRecord:
    tx_type: str
    sku: str
    quantity: int
    timestamp: str = ""
    details: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


# ---- Strategy: Pricing ----

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, base_cost: float, quantity: int,
                  priority: Priority, discount_pct: float) -> float:
        ...


class StandardPricing(PricingStrategy):
    MAX_DISCOUNT_PCT = 50
    URGENT_SURCHARGE = 0.15
    BULK_DISCOUNT = 0.05
    BULK_THRESHOLD = 100

    def calculate(self, base_cost: float, quantity: int,
                  priority: Priority, discount_pct: float) -> float:
        effective_discount = min(discount_pct, self.MAX_DISCOUNT_PCT)
        cost = base_cost * (1 - effective_discount / 100)

        if priority == Priority.URGENT:
            cost *= (1 + self.URGENT_SURCHARGE)
        elif priority == Priority.BULK and quantity >= self.BULK_THRESHOLD:
            cost *= (1 - self.BULK_DISCOUNT)

        return round(cost, 2)


# ---- Observer: Event System ----

class InventoryObserver(Protocol):
    def on_low_stock(self, product: Product, reorder_qty: int) -> None: ...
    def on_order_fulfilled(self, result: OrderResult, product: Product) -> None: ...
    def on_restock(self, product: Product, delta: int) -> None: ...
    def on_transfer(self, product: Product, qty: int,
                    from_wh: str, to_wh: str) -> None: ...


# ---- Core Service ----

class InventoryService:
    LOW_STOCK_THRESHOLD = 5
    REORDER_MULTIPLIER = 3

    def __init__(self, pricing: PricingStrategy):
        self._pricing = pricing
        self._inventory: dict[str, Product] = {}
        self._transactions: list[TransactionRecord] = []
        self._observers: list[InventoryObserver] = []

    def register_observer(self, observer: InventoryObserver) -> None:
        self._observers.append(observer)

    # ---- Commands ----

    def add_product(self, sku: str, name: str, category: str,
                    quantity: int, unit_cost: float,
                    warehouse: str = "main") -> Product:
        if sku in self._inventory:
            product = self._inventory[sku]
            delta = quantity
            product.quantity += quantity
            self._record("restock", sku, delta)
            for obs in self._observers:
                obs.on_restock(product, delta)
            return product

        product = Product(sku=sku, name=name, category=category,
                          quantity=quantity, unit_cost=unit_cost,
                          warehouse=warehouse)
        self._inventory[sku] = product
        self._record("new_product", sku, quantity)
        return product

    def process_order(self, sku: str, quantity: int, customer: str,
                      priority: Priority = Priority.NORMAL,
                      discount_pct: float = 0.0) -> OrderResult:
        if sku not in self._inventory:
            return OrderResult(status="error", sku=sku, reason="not_found")

        product = self._inventory[sku]

        if quantity > product.quantity:
            return self._handle_shortage(product, sku, quantity, priority)

        base_cost = quantity * product.unit_cost
        total = self._pricing.calculate(base_cost, quantity,
                                        priority, discount_pct)

        product.quantity -= quantity
        result = OrderResult(status="fulfilled", sku=sku,
                             quantity=quantity, total=total,
                             customer=customer)

        self._record("order", sku, quantity,
                     {"customer": customer, "total": total})

        for obs in self._observers:
            obs.on_order_fulfilled(result, product)

        if product.quantity <= self.LOW_STOCK_THRESHOLD:
            reorder = self.REORDER_MULTIPLIER * self.LOW_STOCK_THRESHOLD
            for obs in self._observers:
                obs.on_low_stock(product, reorder)

        return result

    def transfer(self, sku: str, from_wh: str, to_wh: str,
                 quantity: int) -> bool:
        if sku not in self._inventory:
            return False
        product = self._inventory[sku]
        if product.warehouse != from_wh or product.quantity < quantity:
            return False

        product.quantity -= quantity
        self._record("transfer", sku, quantity,
                     {"from": from_wh, "to": to_wh})
        for obs in self._observers:
            obs.on_transfer(product, quantity, from_wh, to_wh)
        return True

    # ---- Queries ----

    def get_product(self, sku: str) -> Product | None:
        return self._inventory.get(sku)

    def search(self, query: str,
               search_field: str = "name") -> list[tuple[str, Product]]:
        results = []
        for sku, product in self._inventory.items():
            value = getattr(product, search_field, "")
            if isinstance(value, str) and query.lower() in value.lower():
                results.append((sku, product))
        return results

    def get_summary(self) -> dict:
        categories: dict[str, dict] = {}
        total_items = 0
        total_value = 0.0

        for product in self._inventory.values():
            qty = product.quantity
            val = qty * product.unit_cost
            total_items += qty
            total_value += val

            cat = product.category
            if cat not in categories:
                categories[cat] = {"count": 0, "value": 0.0}
            categories[cat]["count"] += qty
            categories[cat]["value"] += val

        return {
            "total_skus": len(self._inventory),
            "total_items": total_items,
            "total_value": total_value,
            "categories": categories,
        }

    def get_low_stock(self) -> list[tuple[str, Product]]:
        return [(sku, p) for sku, p in self._inventory.items()
                if p.quantity <= self.LOW_STOCK_THRESHOLD]

    def get_valuation(self) -> list[tuple[str, Product, float]]:
        items = [(sku, p, p.quantity * p.unit_cost)
                 for sku, p in self._inventory.items()]
        return sorted(items, key=lambda x: x[2], reverse=True)

    def get_transactions(self, limit: int = 20) -> list[TransactionRecord]:
        return self._transactions[-limit:]

    # ---- Internal ----

    def _handle_shortage(self, product: Product, sku: str,
                         quantity: int,
                         priority: Priority) -> OrderResult:
        available = product.quantity
        if priority == Priority.URGENT:
            return OrderResult(status="partial", sku=sku,
                               quantity=available,
                               shortfall=quantity - available)
        if priority == Priority.BULK:
            return OrderResult(status="rejected", sku=sku,
                               reason="insufficient_stock")
        return OrderResult(status="backorder", sku=sku,
                           shortfall=quantity - available)

    def _record(self, tx_type: str, sku: str, quantity: int,
                details: dict | None = None) -> None:
        self._transactions.append(
            TransactionRecord(tx_type=tx_type, sku=sku,
                              quantity=quantity,
                              details=details or {})
        )
