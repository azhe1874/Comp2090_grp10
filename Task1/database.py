# database.py
import sqlite3
import os
import hashlib
from datetime import datetime


class Database:
    """Handles all database operations (class methods only)."""
    DB_NAME = "warehouse.db"

    @classmethod
    def get_connection(cls):
        return sqlite3.connect(cls.DB_NAME)

    @classmethod
    def initialize(cls):
        """Create tables if they don't exist."""
        print("Initializing database...")
        conn = cls.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT,
                role TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')

        # Suppliers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT,
                categories TEXT
            )
        ''')

        # Items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                item_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                unit_price REAL NOT NULL,
                quantity INTEGER DEFAULT 0,
                min_threshold INTEGER DEFAULT 10,
                item_type TEXT NOT NULL,
                extra_data TEXT
            )
        ''')

        # Warehouses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS warehouses (
                warehouse_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT,
                capacity INTEGER NOT NULL
            )
        ''')

        # Locations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                location_code TEXT PRIMARY KEY,
                aisle TEXT NOT NULL,
                shelf TEXT NOT NULL,
                bin TEXT NOT NULL,
                warehouse_id TEXT NOT NULL,
                FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
            )
        ''')

        # Stock records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                warehouse_id TEXT NOT NULL,
                location_code TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items(item_id),
                FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
                FOREIGN KEY (location_code) REFERENCES locations(location_code)
            )
        ''')

        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                trans_id TEXT PRIMARY KEY,
                trans_type TEXT NOT NULL,
                item_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                operator_id TEXT NOT NULL,
                warehouse_id TEXT NOT NULL,
                location_code TEXT,
                supplier_id TEXT,
                destination TEXT,
                trans_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items(item_id),
                FOREIGN KEY (operator_id) REFERENCES users(user_id),
                FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
            )
        ''')

        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                order_type TEXT NOT NULL,
                status TEXT NOT NULL,
                creator_id TEXT NOT NULL,
                supplier_id TEXT,
                customer_name TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_date TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users(user_id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
            )
        ''')

        # Order items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                order_id TEXT NOT NULL,
                item_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                location_code TEXT,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (item_id) REFERENCES items(item_id)
            )
        ''')

        conn.commit()
        conn.close()
        print("Database initialization complete.")

    @classmethod
    def is_first_run(cls) -> bool:
        """Return True if no users exist in the database."""
        if not os.path.exists(cls.DB_NAME):
            return True
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0

    @classmethod
    def insert_sample_data(cls):
        """Insert sample suppliers, items, warehouse, and locations (no users)."""
        print("Inserting sample data...")
        conn = cls.get_connection()
        cursor = conn.cursor()

        # Sample suppliers
        cursor.execute(
            "INSERT OR IGNORE INTO suppliers VALUES (?, ?, ?, ?)",
            ("S001", "Fresh Fruits Co.", "manager@fresh.com", "Fruits")
        )
        cursor.execute(
            "INSERT OR IGNORE INTO suppliers VALUES (?, ?, ?, ?)",
            ("S002", "Packaging Solutions", "sales@pack.com", "Packaging")
        )

        # Sample items
        cursor.execute(
            "INSERT OR IGNORE INTO items VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("I001", "Apple", 5.0, 100, 20, "Perishable", '{"shelf_life_days": 14}')
        )
        cursor.execute(
            "INSERT OR IGNORE INTO items VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("I002", "Cardboard Box", 2.5, 500, 50, "NonPerishable", '{"warranty_months": 12}')
        )

        # Warehouse
        cursor.execute(
            "INSERT OR IGNORE INTO warehouses VALUES (?, ?, ?, ?)",
            ("WH001", "Main Warehouse", "Shenzhen", 10000)
        )

        # Locations
        cursor.execute(
            "INSERT OR IGNORE INTO locations VALUES (?, ?, ?, ?, ?)",
            ("A-1-01", "A", "1", "01", "WH001")
        )
        cursor.execute(
            "INSERT OR IGNORE INTO locations VALUES (?, ?, ?, ?, ?)",
            ("B-2-03", "B", "2", "03", "WH001")
        )

        # Initial stock
        cursor.execute(
            "INSERT OR IGNORE INTO stock_records (item_id, warehouse_id, location_code, quantity) VALUES (?, ?, ?, ?)",
            ("I001", "WH001", "A-1-01", 80)
        )
        cursor.execute(
            "INSERT OR IGNORE INTO stock_records (item_id, warehouse_id, location_code, quantity) VALUES (?, ?, ?, ?)",
            ("I002", "WH001", "B-2-03", 300)
        )

        conn.commit()
        conn.close()
        print("Sample data inserted.")