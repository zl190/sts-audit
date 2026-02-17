"""
Simple Mall Checkout System — Z-level version - UI / Observer Layer
All print() calls live exclusively in this module.
"""

from service import (
    CheckoutObserver,
    CheckoutResult,
    CheckoutService,
    MemberLevel,
    PercentageProductDiscount,
    Product,
    ShoppingCart,
    User,
)


# ╔══════════════════════════════════════════════════════════════╗
# ║  Observer — Receipt Printer                                 ║
# ╚══════════════════════════════════════════════════════════════╝

class ReceiptPrinter(CheckoutObserver):
    """Pure display, contains no business logic."""

    def on_checkout_completed(self, result: CheckoutResult) -> None:
        w = 42
        lines = [
            "=" * w,
            f"  Checkout - {result.user.name} ({result.user.level.value})",
            "=" * w,
        ]
        for item in result.line_items:
            tag = f" [{item.discount_label}%]" if item.discount_label else ""
            lines.append(
                f"  {item.product_name}{tag}"
                f"  ${item.original_unit_price} x {item.quantity}"
                f"  = ${item.subtotal}"
            )
        rate_pct = result.member_discount_rate * 100
        lines += [
            "-" * w,
            f"  Original Total:     ${result.original_total}",
            f"  After Product Disc: ${result.after_product_discount}",
            f"  Member Discount ({rate_pct:.0f}%): ${result.final_total}",
            f"  Total Saved:        ${result.total_saved}",
            "=" * w,
            f"  Amount Due:         ${result.final_total}",
            "=" * w,
        ]
        print("\n".join(lines))


class CheckoutLogger(CheckoutObserver):
    def on_checkout_completed(self, result: CheckoutResult) -> None:
        print(
            f"[LOG] User {result.user.name} checkout completed, "
            f"amount due ${result.final_total}"
        )


# ╔══════════════════════════════════════════════════════════════╗
# ║  Assembly (Composition Root)                                ║
# ╚══════════════════════════════════════════════════════════════╝

def build_checkout_service() -> CheckoutService:
    service = CheckoutService()
    service.add_observer(ReceiptPrinter())
    service.add_observer(CheckoutLogger())
    return service


# ===================== Demo =====================
if __name__ == "__main__":
    service = build_checkout_service()

    user = User("Bob", MemberLevel.GOLD)

    cart = ShoppingCart()
    cart.add(Product("Mechanical Keyboard", 399), 1)
    cart.add(Product("Wireless Mouse", 129, PercentageProductDiscount(0.8)), 2)
    cart.add(Product("Monitor", 1999, PercentageProductDiscount(0.9)), 1)
    cart.add(Product("USB-C Cable", 29), 3)

    service.checkout(cart, user)
