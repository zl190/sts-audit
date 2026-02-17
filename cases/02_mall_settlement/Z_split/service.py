"""
Simple Mall Checkout System — Z-level version - Service Layer
Pure business logic, zero UI dependencies. View / Observer live in views.py.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


# ╔══════════════════════════════════════════════════════════════╗
# ║  1. Domain Enums                                            ║
# ╚══════════════════════════════════════════════════════════════╝

class MemberLevel(Enum):
    NORMAL = "Regular"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"


# ╔══════════════════════════════════════════════════════════════╗
# ║  2. Strategy Pattern — Product Discount                     ║
# ╚══════════════════════════════════════════════════════════════╝

class ProductDiscountStrategy(ABC):
    @abstractmethod
    def apply(self, base_price: float) -> float: ...

    @abstractmethod
    def label(self) -> str: ...


class NoProductDiscount(ProductDiscountStrategy):
    def apply(self, base_price: float) -> float:
        return base_price

    def label(self) -> str:
        return ""


class PercentageProductDiscount(ProductDiscountStrategy):
    def __init__(self, rate: float):
        self._rate = rate

    def apply(self, base_price: float) -> float:
        return round(base_price * self._rate, 2)

    def label(self) -> str:
        return str(int(self._rate * 100))


# ╔══════════════════════════════════════════════════════════════╗
# ║  3. Strategy Pattern — Member Discount                      ║
# ╚══════════════════════════════════════════════════════════════╝

class MemberDiscountStrategy(ABC):
    @abstractmethod
    def rate(self) -> float: ...


class NormalMemberDiscount(MemberDiscountStrategy):
    def rate(self) -> float:
        return 1.0


class SilverMemberDiscount(MemberDiscountStrategy):
    def rate(self) -> float:
        return 0.95


class GoldMemberDiscount(MemberDiscountStrategy):
    def rate(self) -> float:
        return 0.88


class PlatinumMemberDiscount(MemberDiscountStrategy):
    def rate(self) -> float:
        return 0.80


class MemberDiscountFactory:
    _strategies: dict[MemberLevel, MemberDiscountStrategy] = {
        MemberLevel.NORMAL: NormalMemberDiscount(),
        MemberLevel.SILVER: SilverMemberDiscount(),
        MemberLevel.GOLD: GoldMemberDiscount(),
        MemberLevel.PLATINUM: PlatinumMemberDiscount(),
    }

    @classmethod
    def get(cls, level: MemberLevel) -> MemberDiscountStrategy:
        return cls._strategies[level]


# ╔══════════════════════════════════════════════════════════════╗
# ║  4. Domain Objects                                          ║
# ╚══════════════════════════════════════════════════════════════╝

@dataclass
class Product:
    name: str
    price: float
    discount_strategy: ProductDiscountStrategy = field(
        default_factory=NoProductDiscount,
    )

    @property
    def discounted_price(self) -> float:
        return self.discount_strategy.apply(self.price)


@dataclass
class CartItem:
    product: Product
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        return round(self.product.discounted_price * self.quantity, 2)


@dataclass
class User:
    name: str
    level: MemberLevel = MemberLevel.NORMAL


# ╔══════════════════════════════════════════════════════════════╗
# ║  5. Checkout Result (Value Object)                          ║
# ╚══════════════════════════════════════════════════════════════╝

@dataclass
class CheckoutLineItem:
    product_name: str
    original_unit_price: float
    discounted_unit_price: float
    quantity: int
    discount_label: str
    subtotal: float


@dataclass
class CheckoutResult:
    user: User
    line_items: list[CheckoutLineItem]
    original_total: float
    after_product_discount: float
    member_discount_rate: float
    final_total: float
    total_saved: float


# ╔══════════════════════════════════════════════════════════════╗
# ║  6. Shopping Cart                                           ║
# ╚══════════════════════════════════════════════════════════════╝

class ShoppingCart:
    def __init__(self) -> None:
        self._items: list[CartItem] = []

    def add(self, product: Product, quantity: int = 1) -> None:
        for item in self._items:
            if item.product.name == product.name:
                item.quantity += quantity
                return
        self._items.append(CartItem(product, quantity))

    def remove(self, product_name: str) -> None:
        self._items = [i for i in self._items if i.product.name != product_name]

    @property
    def items(self) -> list[CartItem]:
        return list(self._items)


# ╔══════════════════════════════════════════════════════════════╗
# ║  7. Observer Abstract Contract                              ║
# ╚══════════════════════════════════════════════════════════════╝

class CheckoutObserver(ABC):
    @abstractmethod
    def on_checkout_completed(self, result: CheckoutResult) -> None: ...


# ╔══════════════════════════════════════════════════════════════╗
# ║  8. Core Business — CheckoutService (pure logic, no UI)     ║
# ╚══════════════════════════════════════════════════════════════╝

class CheckoutService:
    def __init__(self) -> None:
        self._observers: list[CheckoutObserver] = []

    def add_observer(self, observer: CheckoutObserver) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer: CheckoutObserver) -> None:
        self._observers.remove(observer)

    def _notify(self, result: CheckoutResult) -> None:
        for obs in self._observers:
            obs.on_checkout_completed(result)

    def checkout(self, cart: ShoppingCart, user: User) -> CheckoutResult:
        member_strategy = MemberDiscountFactory.get(user.level)

        line_items: list[CheckoutLineItem] = []
        original_total = 0.0
        product_discounted_total = 0.0

        for cart_item in cart.items:
            p = cart_item.product
            original = p.price * cart_item.quantity
            subtotal = cart_item.subtotal

            original_total += original
            product_discounted_total += subtotal

            line_items.append(CheckoutLineItem(
                product_name=p.name,
                original_unit_price=p.price,
                discounted_unit_price=p.discounted_price,
                quantity=cart_item.quantity,
                discount_label=p.discount_strategy.label(),
                subtotal=subtotal,
            ))

        member_rate = member_strategy.rate()
        final = round(product_discounted_total * member_rate, 2)
        original_total = round(original_total, 2)
        product_discounted_total = round(product_discounted_total, 2)

        result = CheckoutResult(
            user=user,
            line_items=line_items,
            original_total=original_total,
            after_product_discount=product_discounted_total,
            member_discount_rate=member_rate,
            final_total=final,
            total_saved=round(original_total - final, 2),
        )

        self._notify(result)
        return result
