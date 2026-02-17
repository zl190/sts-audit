"""
Online Bookstore Order System — H-level version v2 (high coupling)
v2 adds: ebook category, extra 5% discount when price > 100 + activation code email.
All logic is still crammed into one class.
"""

import json
import os
import uuid
from datetime import datetime


class OrderProcessor:
    """One class does everything: display, discount, persistence, notification."""

    DB_FILE = "orders_h.json"

    def __init__(self):
        if os.path.exists(self.DB_FILE):
            with open(self.DB_FILE, "r", encoding="utf-8") as f:
                self.orders = json.load(f)
        else:
            self.orders = []

    # ---------- Single public entry point ----------
    def process(self, customer_name: str, customer_email: str,
                items: list[dict]) -> dict:
        """
        items format: [{"title": str, "category": str, "price": float, "qty": int}, ...]
        category in {"fiction", "textbook", "children", "comic", "ebook"}
        """

        # ========== 1. Calculate per-book discount ==========
        total = 0.0
        detail_lines = []
        # v2: track ebooks that need activation codes
        ebook_activation_items = []

        for item in items:
            title = item["title"]
            category = item["category"]
            price = item["price"]
            qty = item["qty"]

            # -- Lengthy if-else discount logic --
            if category == "fiction":
                if qty >= 5:
                    discount = 0.20
                elif qty >= 3:
                    discount = 0.15
                else:
                    discount = 0.10
            elif category == "textbook":
                if qty >= 10:
                    discount = 0.25
                elif qty >= 5:
                    discount = 0.15
                else:
                    discount = 0.05
            elif category == "children":
                if qty >= 5:
                    discount = 0.30
                elif qty >= 3:
                    discount = 0.20
                else:
                    discount = 0.15
            elif category == "comic":
                if qty >= 10:
                    discount = 0.20
                elif qty >= 3:
                    discount = 0.10
                else:
                    discount = 0.05
            # ---- v2: ebook ----
            elif category == "ebook":
                if price > 100:
                    discount = 0.05
                    # Also record ebooks needing activation codes (logic scattered in discount calc)
                    activation_codes = []
                    for _ in range(qty):
                        activation_codes.append(uuid.uuid4().hex[:16].upper())
                    ebook_activation_items.append({
                        "title": title,
                        "qty": qty,
                        "codes": activation_codes,
                    })
                else:
                    discount = 0.0
            # ---- end v2 ----
            else:
                discount = 0.0

            subtotal = price * qty * (1 - discount)
            total += subtotal

            detail_lines.append({
                "title": title,
                "category": category,
                "price": price,
                "qty": qty,
                "discount": f"{discount:.0%}",
                "subtotal": round(subtotal, 2),
            })

        # ========== 2. Order-level threshold discount ==========
        if total >= 500:
            extra_discount = 0.05
        elif total >= 300:
            extra_discount = 0.03
        else:
            extra_discount = 0.0
        final_total = round(total * (1 - extra_discount), 2)

        # ========== 3. Build order record ==========
        order = {
            "order_id": len(self.orders) + 1,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "items": detail_lines,
            "raw_total": round(total, 2),
            "extra_discount": f"{extra_discount:.0%}",
            "final_total": final_total,
            "created_at": datetime.now().isoformat(),
        }

        # ========== 4. Save to "database" (JSON file) ==========
        self.orders.append(order)
        with open(self.DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.orders, f, ensure_ascii=False, indent=2)

        # ========== 5. Send notifications (print directly, tightly coupled) ==========
        print(f"\n[Email] Sent to {customer_email}")
        print(f"  Dear {customer_name}, your order #{order['order_id']} has been confirmed!")
        print(f"  Amount due: ${final_total}")

        print(f"\n[SMS] Sent to {customer_name}")
        print(f"  Order #{order['order_id']} confirmed, amount ${final_total}")

        print(f"\n[Inventory] Internal system")
        for item in detail_lines:
            print(f"  \"{item['title']}\" -- ship {item['qty']} copies")

        # ---- v2: activation code email (yet another notification block crammed in here) ----
        if ebook_activation_items:
            print(f"\n[Activation Email] Sent to {customer_email}")
            for eb in ebook_activation_items:
                print(f"  \"{eb['title']}\" x{eb['qty']} activation codes:")
                for code in eb["codes"]:
                    print(f"    - {code}")
        # ---- end v2 ----

        # ========== 6. Print UI receipt (also coupled here) ==========
        self._print_receipt(order)

        return order

    # ---------- "UI" also lives in this class ----------
    def _print_receipt(self, order: dict):
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


# ===================== Demo =====================
if __name__ == "__main__":
    processor = OrderProcessor()
    processor.process(
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
