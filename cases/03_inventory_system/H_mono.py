"""
Warehouse Inventory Management System — H-level version (high coupling)
All logic (UI display, business rules, reporting, alerting) in one class.
Simulates zero-guidance AI output for inventory management.
"""

import json
import os
from datetime import datetime


class InventoryManager:
    """Single class handling all inventory operations, display, and reporting."""

    DB_FILE = "inventory_h.json"
    LOW_STOCK_THRESHOLD = 5
    REORDER_MULTIPLIER = 3

    def __init__(self):
        if os.path.exists(self.DB_FILE):
            with open(self.DB_FILE, "r", encoding="utf-8") as f:
                self.inventory = json.load(f)
        else:
            self.inventory = {}
        self.transaction_log = []

    def add_product(self, sku: str, name: str, category: str,
                    quantity: int, unit_cost: float, warehouse: str = "main"):
        """Add a new product or update existing stock."""
        if sku in self.inventory:
            old_qty = self.inventory[sku]["quantity"]
            self.inventory[sku]["quantity"] += quantity
            print(f"[RESTOCK] {name} (SKU: {sku}): {old_qty} -> {self.inventory[sku]['quantity']}")
            self.transaction_log.append({
                "type": "restock", "sku": sku, "delta": quantity,
                "timestamp": datetime.now().isoformat()
            })
        else:
            self.inventory[sku] = {
                "name": name, "category": category, "quantity": quantity,
                "unit_cost": unit_cost, "warehouse": warehouse,
                "added": datetime.now().isoformat()
            }
            print(f"[NEW] Added {name} (SKU: {sku}) x{quantity} @ ${unit_cost:.2f}")
            self.transaction_log.append({
                "type": "new_product", "sku": sku, "quantity": quantity,
                "timestamp": datetime.now().isoformat()
            })
        self._save()

    def process_order(self, sku: str, quantity: int, customer: str,
                      priority: str = "normal", discount_pct: float = 0.0):
        """Process an outgoing order with discount and priority handling."""
        if sku not in self.inventory:
            print(f"[ERROR] SKU {sku} not found in inventory!")
            return None

        product = self.inventory[sku]
        available = product["quantity"]

        if quantity > available:
            print(f"[WARN] Insufficient stock for {product['name']}: "
                  f"requested {quantity}, available {available}")
            if priority == "urgent":
                print(f"[URGENT] Partial fulfillment: shipping {available} units")
                quantity = available
            elif priority == "normal":
                print(f"[INFO] Order queued for backorder")
                return {"status": "backorder", "sku": sku, "shortfall": quantity - available}
            elif priority == "bulk":
                print(f"[BULK] Bulk order cannot be partially fulfilled")
                return {"status": "rejected", "reason": "insufficient_stock"}
            else:
                print(f"[ERROR] Unknown priority: {priority}")
                return None

        # Calculate pricing with discount
        base_cost = quantity * product["unit_cost"]
        if discount_pct > 0:
            if discount_pct > 50:
                print(f"[WARN] Discount {discount_pct}% exceeds maximum 50%, capping")
                discount_pct = 50
            discount_amount = base_cost * (discount_pct / 100)
            final_cost = base_cost - discount_amount
            print(f"[DISCOUNT] {discount_pct}% off: ${base_cost:.2f} -> ${final_cost:.2f}")
        else:
            final_cost = base_cost

        # Apply priority surcharge
        if priority == "urgent":
            surcharge = final_cost * 0.15
            final_cost += surcharge
            print(f"[SURCHARGE] Urgent priority: +${surcharge:.2f}")
        elif priority == "bulk" and quantity >= 100:
            bulk_discount = final_cost * 0.05
            final_cost -= bulk_discount
            print(f"[BULK DISCOUNT] -${bulk_discount:.2f}")

        # Update inventory
        product["quantity"] -= quantity
        self._save()

        # Check low stock alert
        if product["quantity"] <= self.LOW_STOCK_THRESHOLD:
            reorder_qty = self.REORDER_MULTIPLIER * self.LOW_STOCK_THRESHOLD
            print(f"\n{'='*50}")
            print(f"  LOW STOCK ALERT: {product['name']}")
            print(f"  Remaining: {product['quantity']} units")
            print(f"  Recommended reorder: {reorder_qty} units")
            print(f"{'='*50}\n")

        # Print receipt
        print(f"\n--- ORDER RECEIPT ---")
        print(f"Customer: {customer}")
        print(f"Product: {product['name']} (SKU: {sku})")
        print(f"Quantity: {quantity}")
        print(f"Unit Cost: ${product['unit_cost']:.2f}")
        print(f"Total: ${final_cost:.2f}")
        print(f"Priority: {priority}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"-------------------\n")

        self.transaction_log.append({
            "type": "order", "sku": sku, "quantity": quantity,
            "customer": customer, "total": final_cost,
            "timestamp": datetime.now().isoformat()
        })

        return {"status": "fulfilled", "sku": sku, "quantity": quantity,
                "total": final_cost, "customer": customer}

    def generate_report(self, report_type: str = "summary"):
        """Generate various inventory reports."""
        if report_type == "summary":
            total_items = sum(p["quantity"] for p in self.inventory.values())
            total_value = sum(p["quantity"] * p["unit_cost"]
                             for p in self.inventory.values())
            categories = {}
            for p in self.inventory.values():
                cat = p["category"]
                if cat not in categories:
                    categories[cat] = {"count": 0, "value": 0.0}
                categories[cat]["count"] += p["quantity"]
                categories[cat]["value"] += p["quantity"] * p["unit_cost"]

            print(f"\n{'='*60}")
            print(f"  INVENTORY SUMMARY REPORT")
            print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            print(f"{'='*60}")
            print(f"  Total SKUs: {len(self.inventory)}")
            print(f"  Total Items: {total_items}")
            print(f"  Total Value: ${total_value:,.2f}")
            print(f"\n  By Category:")
            for cat, data in sorted(categories.items()):
                print(f"    {cat:20s} | {data['count']:6d} items | ${data['value']:>12,.2f}")
            print(f"{'='*60}\n")

        elif report_type == "low_stock":
            low_stock = {sku: p for sku, p in self.inventory.items()
                         if p["quantity"] <= self.LOW_STOCK_THRESHOLD}
            print(f"\n{'='*60}")
            print(f"  LOW STOCK REPORT")
            print(f"{'='*60}")
            if not low_stock:
                print(f"  All items above threshold ({self.LOW_STOCK_THRESHOLD})")
            else:
                for sku, p in low_stock.items():
                    print(f"  [{sku}] {p['name']:30s} | Qty: {p['quantity']:4d} | "
                          f"Warehouse: {p['warehouse']}")
            print(f"{'='*60}\n")

        elif report_type == "valuation":
            print(f"\n{'='*60}")
            print(f"  INVENTORY VALUATION REPORT")
            print(f"{'='*60}")
            items_sorted = sorted(self.inventory.items(),
                                  key=lambda x: x[1]["quantity"] * x[1]["unit_cost"],
                                  reverse=True)
            running_total = 0.0
            for sku, p in items_sorted:
                value = p["quantity"] * p["unit_cost"]
                running_total += value
                print(f"  [{sku}] {p['name']:25s} | {p['quantity']:5d} x "
                      f"${p['unit_cost']:>8.2f} = ${value:>12,.2f}")
            print(f"  {'':25s}   {'Total':>20s} = ${running_total:>12,.2f}")
            print(f"{'='*60}\n")

        elif report_type == "transactions":
            print(f"\n{'='*60}")
            print(f"  TRANSACTION LOG ({len(self.transaction_log)} entries)")
            print(f"{'='*60}")
            for i, tx in enumerate(self.transaction_log[-20:], 1):
                print(f"  {i:3d}. [{tx['type']:12s}] SKU: {tx['sku']} | "
                      f"{tx['timestamp']}")
            print(f"{'='*60}\n")
        else:
            print(f"[ERROR] Unknown report type: {report_type}")
            print(f"Available: summary, low_stock, valuation, transactions")

    def warehouse_transfer(self, sku: str, from_wh: str, to_wh: str,
                           quantity: int):
        """Transfer stock between warehouses."""
        if sku not in self.inventory:
            print(f"[ERROR] SKU {sku} not found")
            return False
        product = self.inventory[sku]
        if product["warehouse"] != from_wh:
            print(f"[ERROR] {product['name']} is in {product['warehouse']}, not {from_wh}")
            return False
        if product["quantity"] < quantity:
            print(f"[ERROR] Insufficient stock: {product['quantity']} < {quantity}")
            return False
        product["quantity"] -= quantity
        # In a real system, we'd track multi-warehouse; here we just log it
        print(f"[TRANSFER] {product['name']} x{quantity}: {from_wh} -> {to_wh}")
        self.transaction_log.append({
            "type": "transfer", "sku": sku, "quantity": quantity,
            "from": from_wh, "to": to_wh,
            "timestamp": datetime.now().isoformat()
        })
        self._save()
        return True

    def _save(self):
        with open(self.DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.inventory, f, indent=2)

    def search(self, query: str, field: str = "name"):
        """Search inventory by name, category, or warehouse."""
        results = []
        for sku, product in self.inventory.items():
            if field == "name" and query.lower() in product["name"].lower():
                results.append((sku, product))
            elif field == "category" and query.lower() == product["category"].lower():
                results.append((sku, product))
            elif field == "warehouse" and query.lower() == product["warehouse"].lower():
                results.append((sku, product))

        if results:
            print(f"\n  Search results for '{query}' in {field}:")
            for sku, p in results:
                print(f"  [{sku}] {p['name']:25s} | Qty: {p['quantity']:5d} | "
                      f"${p['unit_cost']:.2f} | {p['warehouse']}")
        else:
            print(f"  No results for '{query}' in {field}")
        return results


# ---------- demo ----------
if __name__ == "__main__":
    mgr = InventoryManager()

    # Add products
    mgr.add_product("ELEC-001", "Wireless Mouse", "electronics", 150, 24.99)
    mgr.add_product("ELEC-002", "USB-C Hub", "electronics", 80, 45.00)
    mgr.add_product("FURN-001", "Standing Desk", "furniture", 25, 299.99)
    mgr.add_product("FURN-002", "Ergonomic Chair", "furniture", 40, 449.99)
    mgr.add_product("OFFC-001", "Notebook Pack (12)", "office", 200, 8.99)
    mgr.add_product("OFFC-002", "Whiteboard Markers", "office", 3, 12.50)

    # Process orders
    mgr.process_order("ELEC-001", 10, "Acme Corp", priority="normal")
    mgr.process_order("FURN-001", 5, "Beta Inc", priority="urgent", discount_pct=10)
    mgr.process_order("OFFC-002", 2, "Charlie LLC", priority="normal")

    # Reports
    mgr.generate_report("summary")
    mgr.generate_report("low_stock")

    # Transfer
    mgr.warehouse_transfer("ELEC-002", "main", "west", 20)

    # Search
    mgr.search("desk", "name")
