# controller.py
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from database import Database
from models import (
    User, UserRole, Item, PerishableItem, NonPerishableItem,
    InsufficientStockError, InvalidOperationError
)
from utils import Utils


class InventoryController:
    """Main business logic controller for warehouse operations."""

    def __init__(self):
        self._current_user: Optional[User] = None
        Database.initialize()

    def login(self, username: str, password: str) -> bool:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, name, contact, role, password_hash FROM users WHERE user_id = ?",
            (username,)
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            return False
        pass_hash = Utils.hash_password(password)
        if pass_hash != row[4]:
            return False
        role = UserRole.ADMIN if row[3] == "admin" else UserRole.STAFF
        self._current_user = User(row[0], row[1], row[2], role)
        return True

    def logout(self):
        self._current_user = None

    def get_current_user(self) -> Optional[User]:
        return self._current_user

    def create_user(self, user_id: str, name: str, contact: str, role: str, password: str) -> bool:
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            pass_hash = Utils.hash_password(password)
            cursor.execute(
                "INSERT INTO users (user_id, name, contact, role, password_hash) VALUES (?, ?, ?, ?, ?)",
                (user_id, name, contact, role, pass_hash)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_items(self) -> List[Tuple]:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT item_id, name, unit_price, quantity, min_threshold, item_type FROM items ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_item(self, item_id: str, name: str, price: float, qty: int, threshold: int,
                 item_type: str, extra: str) -> bool:
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?)",
                (item_id, name, price, qty, threshold, item_type, extra)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_item(self, item_id: str, name: str, price: float, threshold: int, extra: str) -> bool:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE items SET name = ?, unit_price = ?, min_threshold = ?, extra_data = ? WHERE item_id = ?",
            (name, price, threshold, extra, item_id)
        )
        conn.commit()
        conn.close()
        return True

    def delete_item(self, item_id: str) -> bool:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
        conn.commit()
        conn.close()
        return True

    def get_all_suppliers(self) -> List[Tuple]:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT supplier_id, name, contact, categories FROM suppliers ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_supplier(self, sup_id: str, name: str, contact: str, categories: str) -> bool:
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO suppliers VALUES (?, ?, ?, ?)",
                (sup_id, name, contact, categories)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_warehouses(self) -> List[Tuple]:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT warehouse_id, name FROM warehouses")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_locations(self, warehouse_id: str) -> List[str]:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT location_code FROM locations WHERE warehouse_id = ? ORDER BY location_code",
            (warehouse_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [r[0] for r in rows]

    def inbound(self, item_id: str, qty: int, warehouse_id: str, location_code: str,
                supplier_id: str = None) -> bool:
        if not self._current_user:
            return False

        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT capacity FROM warehouses WHERE warehouse_id = ?", (warehouse_id,))
            cap = cursor.fetchone()[0]
            cursor.execute(
                "SELECT SUM(quantity) FROM stock_records WHERE warehouse_id = ?",
                (warehouse_id,)
            )
            used = cursor.fetchone()[0] or 0
            if used + qty > cap:
                raise InvalidOperationError("Warehouse capacity exceeded")

            cursor.execute("UPDATE items SET quantity = quantity + ? WHERE item_id = ?", (qty, item_id))

            cursor.execute('''
                SELECT record_id, quantity FROM stock_records
                WHERE item_id = ? AND warehouse_id = ? AND location_code = ?
            ''', (item_id, warehouse_id, location_code))
            existing = cursor.fetchone()
            if existing:
                cursor.execute(
                    "UPDATE stock_records SET quantity = quantity + ?, last_updated = CURRENT_TIMESTAMP WHERE record_id = ?",
                    (qty, existing[0])
                )
            else:
                cursor.execute(
                    "INSERT INTO stock_records (item_id, warehouse_id, location_code, quantity) VALUES (?, ?, ?, ?)",
                    (item_id, warehouse_id, location_code, qty)
                )

            trans_id = Utils.generate_transaction_id("T")
            cursor.execute(
                "INSERT INTO transactions (trans_id, trans_type, item_id, quantity, operator_id, warehouse_id, location_code, supplier_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (trans_id, "in", item_id, qty, self._current_user.get_id(), warehouse_id, location_code, supplier_id)
            )

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def outbound(self, item_id: str, qty: int, warehouse_id: str, location_code: str = None) -> bool:
        if not self._current_user:
            return False

        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT quantity FROM items WHERE item_id = ?", (item_id,))
            total = cursor.fetchone()
            if not total or total[0] < qty:
                raise InsufficientStockError("Insufficient total stock")

            if location_code:
                cursor.execute(
                    "SELECT quantity FROM stock_records WHERE item_id = ? AND warehouse_id = ? AND location_code = ?",
                    (item_id, warehouse_id, location_code)
                )
                loc_qty = cursor.fetchone()
                if not loc_qty or loc_qty[0] < qty:
                    raise InsufficientStockError("Insufficient stock at specified location")
                cursor.execute(
                    "UPDATE stock_records SET quantity = quantity - ? WHERE item_id = ? AND warehouse_id = ? AND location_code = ?",
                    (qty, item_id, warehouse_id, location_code)
                )
            else:
                cursor.execute(
                    "SELECT location_code, quantity FROM stock_records WHERE item_id = ? AND warehouse_id = ? AND quantity > 0 ORDER BY location_code",
                    (item_id, warehouse_id)
                )
                locations = cursor.fetchall()
                remaining = qty
                for loc, loc_qty in locations:
                    take = min(remaining, loc_qty)
                    cursor.execute(
                        "UPDATE stock_records SET quantity = quantity - ? WHERE item_id = ? AND warehouse_id = ? AND location_code = ?",
                        (take, item_id, warehouse_id, loc)
                    )
                    remaining -= take
                    if remaining == 0:
                        break
                if remaining > 0:
                    raise InsufficientStockError("Insufficient stock across locations")

            cursor.execute("UPDATE items SET quantity = quantity - ? WHERE item_id = ?", (qty, item_id))

            trans_id = Utils.generate_transaction_id("T")
            cursor.execute(
                "INSERT INTO transactions (trans_id, trans_type, item_id, quantity, operator_id, warehouse_id, location_code) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (trans_id, "out", item_id, qty, self._current_user.get_id(), warehouse_id, location_code)
            )

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_recent_transactions(self, limit: int = 50) -> List[Tuple]:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.trans_id, t.trans_type, i.name, t.quantity, u.name, t.trans_date
            FROM transactions t
            JOIN items i ON t.item_id = i.item_id
            JOIN users u ON t.operator_id = u.user_id
            ORDER BY t.trans_date DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_inventory_summary(self) -> Dict:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        item_count = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(quantity * unit_price) FROM items")
        total_value = cursor.fetchone()[0] or 0.0
        cursor.execute("SELECT COUNT(*) FROM items WHERE quantity < min_threshold")
        low_stock_count = cursor.fetchone()[0]
        conn.close()
        return {
            "total_items": item_count,
            "total_value": round(total_value, 2),
            "low_stock_count": low_stock_count
        }

    def get_low_stock_alerts(self) -> List[str]:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity, min_threshold FROM items WHERE quantity < min_threshold")
        rows = cursor.fetchall()
        conn.close()
        return [f"{name} (Qty: {qty} < Min: {threshold})" for name, qty, threshold in rows]


    def get_item_details_extra(self, item_id: str) -> Dict:
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.trans_id, t.trans_type, t.quantity, u.name, t.trans_date, IFNULL(s.name, 'Normal supplier')
            FROM transactions t
            JOIN users u ON t.operator_id = u.user_id
            LEFT JOIN suppliers s ON t.supplier_id = s.supplier_id
            WHERE t.item_id = ?
            ORDER BY t.trans_date DESC
        ''', (item_id,))
        history = cursor.fetchall()
        

        cursor.execute('''
            SELECT DISTINCT s.name
            FROM transactions t
            JOIN suppliers s ON t.supplier_id = s.supplier_id
            WHERE t.item_id = ? AND t.trans_type = 'in'
        ''', (item_id,))
        sups = [r[0] for r in cursor.fetchall()]
        suppliers_str = ", ".join(sups) if sups else "Normal supplier"
        
        conn.close()
        return {"history": history, "suppliers": suppliers_str}

    def get_supplier_supplied_items(self, supplier_id: str) -> List[Tuple]:
        conn = Database.get_connection()
        cursor = conn.cursor()
        

        cursor.execute('''
            SELECT i.item_id, i.name, SUM(t.quantity) as total_supplied
            FROM transactions t
            JOIN items i ON t.item_id = i.item_id
            WHERE t.supplier_id = ? AND t.trans_type = 'in'
            GROUP BY i.item_id, i.name
            ORDER BY total_supplied DESC
        ''', (supplier_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows