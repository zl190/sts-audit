"""Simple Mall Checkout System — supports member tiers and discounts"""

from dataclasses import dataclass, field
from enum import Enum


class MemberLevel(Enum):
    NORMAL = "Regular"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"


# Member discount rates
MEMBER_DISCOUNTS = {
    MemberLevel.NORMAL: 1.0,
    MemberLevel.SILVER: 0.95,
    MemberLevel.GOLD: 0.88,
    MemberLevel.PLATINUM: 0.80,
}


@dataclass
class Product:
    name: str
    price: float
    discount: float = 1.0  # Product-level discount; 1.0 means no discount

    @property
    def discounted_price(self) -> float:
        return round(self.price * self.discount, 2)


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

    @property
    def discount_rate(self) -> float:
        return MEMBER_DISCOUNTS[self.level]


@dataclass
class ShoppingCart:
    user: User
    items: list[CartItem] = field(default_factory=list)

    def add(self, product: Product, quantity: int = 1):
        for item in self.items:
            if item.product.name == product.name:
                item.quantity += quantity
                return
        self.items.append(CartItem(product, quantity))

    def remove(self, product_name: str):
        self.items = [i for i in self.items if i.product.name != product_name]

    @property
    def original_total(self) -> float:
        """Original price total before any discounts"""
        return round(sum(i.product.price * i.quantity for i in self.items), 2)

    @property
    def after_product_discount(self) -> float:
        """Total after product-level discounts"""
        return round(sum(i.subtotal for i in self.items), 2)

    @property
    def final_total(self) -> float:
        """Final price after stacking member discount"""
        return round(self.after_product_discount * self.user.discount_rate, 2)

    @property
    def total_saved(self) -> float:
        return round(self.original_total - self.final_total, 2)

    def checkout(self) -> str:
        lines = [
            f"{'=' * 42}",
            f"  Checkout - {self.user.name} ({self.user.level.value})",
            f"{'=' * 42}",
        ]
        for item in self.items:
            tag = f" [{(1 - item.product.discount) * 100:.0f}% off]" if item.product.discount < 1 else ""
            lines.append(
                f"  {item.product.name}{tag}"
                f"  ${item.product.price} x {item.quantity}"
                f"  = ${item.subtotal}"
            )
        lines += [
            f"{'-' * 42}",
            f"  Original Total:     ${self.original_total}",
            f"  After Product Disc: ${self.after_product_discount}",
            f"  Member Discount ({self.user.discount_rate * 100:.0f}%): ${self.final_total}",
            f"  Total Saved:        ${self.total_saved}",
            f"{'=' * 42}",
            f"  Amount Due:         ${self.final_total}",
            f"{'=' * 42}",
        ]
        return "\n".join(lines)


# ---- Demo ----
if __name__ == "__main__":
    user = User("Bob", MemberLevel.GOLD)

    products = [
        Product("Mechanical Keyboard", 399),
        Product("Wireless Mouse", 129, discount=0.8),   # 20% off
        Product("Monitor", 1999, discount=0.9),          # 10% off
        Product("USB-C Cable", 29),
    ]

    cart = ShoppingCart(user)
    cart.add(products[0], 1)
    cart.add(products[1], 2)
    cart.add(products[2], 1)
    cart.add(products[3], 3)

    print(cart.checkout())
