"""
Warehouse Inventory Management System — Z-level views (presentation layer)
All print/display logic lives here. Imports service for business logic.
"""

from datetime import datetime
from service import (
    InventoryService, StandardPricing, Priority,
    Product, OrderResult, InventoryObserver,
)


class ConsoleDisplay(InventoryObserver):
    """Observer that renders all events to console."""

    def on_low_stock(self, product: Product, reorder_qty: int) -> None:
        print(f"\n{'='*50}")
        print(f"  LOW STOCK ALERT: {product.name}")
        print(f"  Remaining: {product.quantity} units")
        print(f"  Recommended reorder: {reorder_qty} units")
        print(f"{'='*50}\n")

    def on_order_fulfilled(self, result: OrderResult,
                           product: Product) -> None:
        print(f"\n--- ORDER RECEIPT ---")
        print(f"Customer: {result.customer}")
        print(f"Product: {product.name} (SKU: {result.sku})")
        print(f"Quantity: {result.quantity}")
        print(f"Unit Cost: ${product.unit_cost:.2f}")
        print(f"Total: ${result.total:.2f}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"-------------------\n")

    def on_restock(self, product: Product, delta: int) -> None:
        print(f"[RESTOCK] {product.name} (SKU: {product.sku}): "
              f"+{delta} -> {product.quantity}")

    def on_transfer(self, product: Product, qty: int,
                    from_wh: str, to_wh: str) -> None:
        print(f"[TRANSFER] {product.name} x{qty}: {from_wh} -> {to_wh}")


def print_summary(service: InventoryService) -> None:
    summary = service.get_summary()
    print(f"\n{'='*60}")
    print(f"  INVENTORY SUMMARY REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"  Total SKUs: {summary['total_skus']}")
    print(f"  Total Items: {summary['total_items']}")
    print(f"  Total Value: ${summary['total_value']:,.2f}")
    print(f"\n  By Category:")
    for cat, data in sorted(summary["categories"].items()):
        print(f"    {cat:20s} | {data['count']:6d} items | "
              f"${data['value']:>12,.2f}")
    print(f"{'='*60}\n")


def print_low_stock(service: InventoryService) -> None:
    low = service.get_low_stock()
    print(f"\n{'='*60}")
    print(f"  LOW STOCK REPORT")
    print(f"{'='*60}")
    if not low:
        print(f"  All items above threshold")
    else:
        for sku, p in low:
            print(f"  [{sku}] {p.name:30s} | Qty: {p.quantity:4d} | "
                  f"Warehouse: {p.warehouse}")
    print(f"{'='*60}\n")


# ---------- demo ----------
if __name__ == "__main__":
    service = InventoryService(pricing=StandardPricing())
    display = ConsoleDisplay()
    service.register_observer(display)

    # Add products
    service.add_product("ELEC-001", "Wireless Mouse", "electronics",
                        150, 24.99)
    service.add_product("ELEC-002", "USB-C Hub", "electronics", 80, 45.00)
    service.add_product("FURN-001", "Standing Desk", "furniture", 25, 299.99)
    service.add_product("FURN-002", "Ergonomic Chair", "furniture",
                        40, 449.99)
    service.add_product("OFFC-001", "Notebook Pack (12)", "office",
                        200, 8.99)
    service.add_product("OFFC-002", "Whiteboard Markers", "office",
                        3, 12.50)

    # Process orders
    service.process_order("ELEC-001", 10, "Acme Corp")
    service.process_order("FURN-001", 5, "Beta Inc",
                          priority=Priority.URGENT, discount_pct=10)
    service.process_order("OFFC-002", 2, "Charlie LLC")

    # Reports
    print_summary(service)
    print_low_stock(service)

    # Transfer
    service.transfer("ELEC-002", "main", "west", 20)

    # Search
    results = service.search("desk")
    if results:
        print(f"\n  Search results:")
        for sku, p in results:
            print(f"  [{sku}] {p.name:25s} | Qty: {p.quantity:5d} | "
                  f"${p.unit_cost:.2f}")
