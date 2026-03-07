# Task 1

## Objective
This project aims to develop a Warehouse Management System (WMS) to address inventory tracking challenges. The primary objective is to design a foundational, object-oriented software model that can manage core entities like items, stock levels, users, and transactions. The focus is on applying fundamental Object-Oriented Programming (OOP) principles to create a modular, maintainable, and extensible system architecture as a preliminary step toward a full-featured application, potentially with a graphical interface later.

## OOP Concepts Utilized
- **Encapsulation:** This is consistently applied across all classes. Attributes like `_item_id`, `_quantity`, and `_role` are marked as private (using a leading underscore) to restrict direct access. Instead, public getter methods (e.g., `get_item_id()`) and setter methods (e.g., `set_quantity()`) are provided. This protects the integrity of the data by allowing the class to control how its attributes are viewed and modified. For example, the `set_quantity` method in the `Item` class includes a validation check to prevent the stock from being set to a negative number.
- **Inheritance:** While not heavily utilized in the current implementation, the groundwork is laid. The structure suggests that future expansions could use inheritance. For instance, an `Item` class could be a parent to specialized classes like `PerishableItem` (with an added `expiry_date` attribute) or `ElectronicsItem` (with a `warranty_period`). Similarly, the `User` class is designed to be a parent, with the `role` attribute determining permissions, which could be further refined by creating `Admin` and `Staff` subclasses.
- **Polymorphism:** The design allows for polymorphism, particularly through the `User.can_perform()` method. While not using method overriding with subclasses, the same method call (`can_perform()`) exhibits different behaviors based on the object's internal state (`_role`). An `admin` user and a `staff` user will get different results for the same action (e.g., `delete_user`). This is a form of polymorphism where objects of the same class can behave differently.
- **Abstraction:** The system uses abstraction to hide complex implementation details behind simple interfaces. For example, to process an inventory transaction, a user only needs to create a `Transaction` object and call its `process()` method. The intricate logic of checking stock levels (for outbound), updating the `Item`'s quantity, and recording the transaction's date is all hidden within that single method. The `Transaction` class provides a clean, abstract interface for this operation.

## Classes Implemented
- **Class `Item`:** This class represents a product stored in the warehouse. Its attributes include a unique ID (`_item_id`), name (`_name`), price (`_unit_price`), and current stock level (`_quantity`). It uses encapsulation by keeping its attributes private and controlling access and modification via getters and methods like `add_quantity()` and `reduce_quantity()`. This ensures the stock level is managed safely and consistently (e.g., cannot be reduced below zero).
- **Class `Supplier`:** This class stores information about the vendors who supply the items. It holds the supplier's ID (`_supplier_id`), name (`_name`), and contact details (`_contact`). It primarily serves as a data container with getter methods, demonstrating basic encapsulation.
- **Class `Location`:** This class defines a specific physical storage position within a warehouse using an aisle (`_aisle`), shelf (`_shelf`), and bin (`_bin`). It is a simple class used to precisely identify where an item is stored.
- **Class `StockRecord`:** This class establishes a relationship between an `Item`, a `Warehouse`, and a `Location`. It records the `_quantity` of a specific item at a specific spot and timestamps the last update (`_last_updated`). This allows for more granular tracking than just an item's total stock.
- **Class `Warehouse`:** This class represents a physical warehouse location. It has an ID (`_warehouse_id`), a location description, a storage capacity, and importantly, a list of `StockRecord` objects. Its methods, `add_stock()` and `remove_stock()`, provide a high-level interface for managing inventory within that specific warehouse.
- **Class `Transaction`:** This class models an inventory movement event. It captures the ID (`_trans_id`), the `Item` involved, the `_quantity`, the `User` who performed it, the `_type` ("in" or "out"), and the `_date`. The core logic for inbound and outbound operations is contained in its `process()` method, which updates the associated `Item`'s stock.
- **Class `User`:** This class represents a person interacting with the WMS. It stores a user ID, name, and role. Its key method is `can_perform()`, which encapsulates the permission logic, determining if a user with a given role (`admin` or `staff`) is authorized to perform a specific action. This centralizes authorization rules within the class itself.

## How to Run the Code (Preliminary)
1.  Save the provided Python code as a file, for example, `comp2090_group10.py`.
2.  Open a terminal or command prompt and navigate to the directory where you saved the file.
3.  Run the script using the Python interpreter:
    ```bash
    python comp2090_group10.py
    ```
4.  The script will execute the example usage in the `if __name__ == "__main__":` block and print the results to the console. There is no interactive prompt in this preliminary version.

## Current Status / Limitations
- The code currently handles basic object modeling and simple transaction logic for demonstration purposes. It successfully creates objects and simulates inbound/outbound operations.
- Data is stored entirely in memory (RAM). All objects and their states are lost when the program terminates. There is no persistence to a file or database.
- Error handling is minimal. While some methods check for conditions like insufficient stock, the system lacks comprehensive `try-except` blocks to gracefully handle unexpected inputs or runtime errors.
- The user interface is non-existent beyond a hardcoded example in the main block. It is purely a backend logic demonstration and not an interactive application.
- The `Warehouse.add_stock()` method has a simple implementation that creates a new `StockRecord` every time, even for an item already in the warehouse. A more robust system would check for an existing record and update it, rather than creating a duplicate.
