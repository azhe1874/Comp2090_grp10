# Warehouse Management System (WMS)

## Project Overview

The **Warehouse Management System (WMS)** is a Python-based desktop application designed to address common inventory tracking challenges faced by warehouses and distribution centers. The system provides a user-friendly graphical interface for managing stock levels, processing inbound/outbound transactions, handling suppliers, and supporting multi-warehouse operations with location-level granularity.

The primary goal of this project is to demonstrate the application of **Object-Oriented Programming (OOP)** principles—such as encapsulation, inheritance, polymorphism, and abstraction—to create a modular, maintainable, and extensible software architecture.

---

## Key Features

- **User Authentication & Role Management**  
  - Admin and Staff roles with different access levels.  
  - Secure password hashing using SHA-256.

- **Inventory Management**  
  - Add, edit, delete, and view items.  
  - Support for **Perishable** (with expiration tracking) and **Non-Perishable** items.  
  - Automatic low-stock alerts based on configurable thresholds.

- **Warehouse & Location Management**  
  - Multiple warehouses with capacity limits.  
  - Fine-grained storage locations (aisle-shelf-bin).  
  - Real-time stock tracking per location.

- **Transaction Processing**  
  - **Inbound** (receiving stock) from suppliers.  
  - **Outbound** (shipping stock) to customers, with optional location selection or automatic location picking.  
  - Transaction history with operator logging.

- **Supplier Management**  
  - Maintain supplier contact information and product categories.

- **Reporting & Monitoring**  
  - Dashboard with inventory summary (total items, total value, low stock count).  
  - Recent transaction history.  
  - Low stock alerts.

---

## Technology Stack

| Component       | Technology                          |
|----------------|-------------------------------------|
| Language       | Python 3                            |
| GUI Framework  | Tkinter / ttk                       |
| Database       | SQLite3                             |
| Architecture   | Model-View-Controller (MVC) pattern |
| Authentication | SHA-256 password hashing            |

---
## Project Structure (Key Modules)
- main.py `Application entry point`
- gui.py `Tkinter-based user interface (Views)`
- controller.py `Business logic & transaction orchestration (Controller)`
- models.py `OOP domain models (User, Item, Warehouse, etc.)`
- database.py `Database initialization and connection handling`
- utils.py `Utility functions (hashing, validation, formatting)`
-  warehouse.db `SQLite database file (auto-generated)`
---

## Object-Oriented Design Highlights

### 1. **Encapsulation**
- Each class (`User`, `Item`, `Warehouse`, etc.) protects its internal state using private attributes (e.g., `_name`, `_quantity`).
- Getter/setter methods control access to sensitive data.

### 2. **Inheritance & Polymorphism**
- `Person` abstract base class → `User` and `Supplier` concrete classes.
- `Item` abstract base class → `PerishableItem` and `NonPerishableItem` subclasses.
- Polymorphic methods like `get_item_type()` and `check_stock_status()` behave differently per subclass.

### 3. **Abstraction**
- Abstract methods in base classes enforce a consistent interface across all derived types.
- The controller layer hides database and business logic complexity from the GUI.

### 4. **Exception Handling**
- Custom exceptions (`InsufficientStockError`, `InvalidOperationError`) provide meaningful error feedback.

---

## Database Schema (SQLite)

The system uses the following main tables:

- `users` – User credentials and roles.
- `items` – Product catalog with type-specific extra data stored as JSON.
- `warehouses` – Physical warehouse details.
- `locations` – Storage positions within warehouses.
- `stock_records` – Current stock levels per item/warehouse/location.
- `transactions` – Complete audit log of all inbound/outbound movements.
- `suppliers` – Vendor information.
- `orders` & `order_items` – Support for purchase/sales orders (extensible).

---

## Setup & Installation

### Prerequisites
- Python 3.7 or higher
- Tkinter (usually included with Python, but may need separate install on Linux)

### Installation Steps

1. **Clone or download** the project files into a local directory.

2. **Install dependencies** (no external packages required beyond Python standard library).

3. **Run the application**:
   ```bash
   python main.py

📺 **Watch the 5-minute introduction video here:**
👉

## Current Status / Limitations
- The code currently handles basic object modeling and simple transaction logic for demonstration purposes. It successfully creates objects and simulates inbound/outbound operations.
- Data is stored entirely in memory (RAM). All objects and their states are lost when the program terminates. There is no persistence to a file or database.
- Error handling is minimal. While some methods check for conditions like insufficient stock, the system lacks comprehensive `try-except` blocks to gracefully handle unexpected inputs or runtime errors.
- The user interface is non-existent beyond a hardcoded example in the main block. It is purely a backend logic demonstration and not an interactive application.
- The `Warehouse.add_stock()` method has a simple implementation that creates a new `StockRecord` every time, even for an item already in the warehouse. A more robust system would check for an existing record and update it, rather than creating a duplicate.
