# models.py
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


# ==================== Exceptions ====================
class StockException(Exception):
    """Base exception for stock-related errors."""
    pass


class InsufficientStockError(StockException):
    """Raised when requested quantity exceeds available stock."""
    pass


class InvalidOperationError(StockException):
    """Raised when an operation cannot be performed."""
    pass


# ==================== Enums ====================
class UserRole(Enum):
    ADMIN = "admin"
    STAFF = "staff"


class TransactionType(Enum):
    INBOUND = "in"
    OUTBOUND = "out"


class OrderStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# ==================== Abstract Base Classes ====================
class Person(ABC):
    """Abstract base class for all persons in the system."""
    def __init__(self, person_id: str, name: str, contact: str):
        self._person_id = person_id
        self._name = name
        self._contact = contact

    def get_id(self) -> str:
        return self._person_id

    def get_name(self) -> str:
        return self._name

    def get_contact(self) -> str:
        return self._contact

    @abstractmethod
    def get_role(self) -> str:
        """Return the role of the person as a string."""
        pass

    def __str__(self) -> str:
        """Magic method: string representation of a Person."""
        return f"{self._name} ({self._person_id})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self._person_id}>"


class Item(ABC):
    """Abstract base class for all inventory items."""
    def __init__(self, item_id: str, name: str, unit_price: float, quantity: int = 0):
        self._item_id = item_id
        self._name = name
        self._unit_price = unit_price
        self._quantity = quantity
        self._min_threshold = 10

    def get_id(self) -> str:
        return self._item_id

    def get_name(self) -> str:
        return self._name

    def get_unit_price(self) -> float:
        return self._unit_price

    def get_quantity(self) -> int:
        return self._quantity

    def set_quantity(self, qty: int):
        if qty >= 0:
            self._quantity = qty
        else:
            raise ValueError("Quantity cannot be negative")

    def get_min_threshold(self) -> int:
        return self._min_threshold

    def set_min_threshold(self, threshold: int):
        self._min_threshold = threshold

    def is_low_stock(self) -> bool:
        return self._quantity < self._min_threshold

    @abstractmethod
    def get_item_type(self) -> str:
        """Return the type of item as a string."""
        pass

    @abstractmethod
    def check_stock_status(self) -> str:
        """Return a human-readable status string."""
        pass

    def __str__(self) -> str:
        """Magic method: readable string representation."""
        return f"{self._name} (ID: {self._item_id}) - Qty: {self._quantity}, Price: ${self._unit_price:.2f}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self._item_id}>"


# ==================== Concrete Classes ====================
class User(Person):
    """Concrete user class."""
    def __init__(self, user_id: str, name: str, contact: str, role: UserRole):
        super().__init__(user_id, name, contact)
        self._role = role

    def get_role(self) -> str:
        return self._role.value

    def get_user_role(self) -> UserRole:
        return self._role

    def can_perform(self, action: str) -> bool:
        if self._role == UserRole.ADMIN:
            return True
        elif self._role == UserRole.STAFF:
            return action in ["view_stock", "create_transaction", "view_orders"]
        return False

    def __eq__(self, other) -> bool:
        """Magic method: compare two users by ID."""
        if not isinstance(other, User):
            return False
        return self._person_id == other._person_id


class Supplier(Person):
    """Concrete supplier class."""
    def __init__(self, supplier_id: str, name: str, contact: str, categories: str = ""):
        super().__init__(supplier_id, name, contact)
        self._categories = categories

    def get_role(self) -> str:
        return "supplier"

    def get_categories(self) -> str:
        return self._categories

    def __str__(self) -> str:
        return f"{self._name} (Supplier: {self._person_id}) - Categories: {self._categories}"


class PerishableItem(Item):
    """Item with expiration date."""
    def __init__(self, item_id: str, name: str, unit_price: float, quantity: int,
                 production_date: datetime = None, shelf_life_days: int = 14):
        super().__init__(item_id, name, unit_price, quantity)
        self._production_date = production_date or datetime.now()
        self._shelf_life_days = shelf_life_days

    def get_item_type(self) -> str:
        return "Perishable"

    def check_stock_status(self) -> str:
        base = f"{self._name}: {self._quantity} units"
        if self.is_low_stock():
            base += " (LOW STOCK)"
        days_left = self.days_until_expiry()
        if days_left <= 0:
            base += " [EXPIRED]"
        elif days_left <= 3:
            base += f" [Expires in {days_left} days]"
        return base

    def days_until_expiry(self) -> int:
        expiry = self._production_date + timedelta(days=self._shelf_life_days)
        return (expiry - datetime.now()).days

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} (Perishable, Expires in {self.days_until_expiry()} days)"


class NonPerishableItem(Item):
    """Item without expiration."""
    def __init__(self, item_id: str, name: str, unit_price: float, quantity: int,
                 warranty_months: int = 12):
        super().__init__(item_id, name, unit_price, quantity)
        self._warranty_months = warranty_months

    def get_item_type(self) -> str:
        return "NonPerishable"

    def check_stock_status(self) -> str:
        base = f"{self._name}: {self._quantity} units"
        if self.is_low_stock():
            base += " (LOW STOCK)"
        return base

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} (Non-perishable, Warranty: {self._warranty_months} months)"


class Location:
    """Represents a storage location within a warehouse."""
    def __init__(self, aisle: str, shelf: str, bin_code: str):
        self.aisle = aisle
        self.shelf = shelf
        self.bin = bin_code

    def get_code(self) -> str:
        return f"{self.aisle}-{self.shelf}-{self.bin}"

    def __str__(self) -> str:
        return self.get_code()

    def __repr__(self) -> str:
        return f"Location('{self.aisle}', '{self.shelf}', '{self.bin}')"


class Warehouse:
    """Represents a physical warehouse."""
    def __init__(self, warehouse_id: str, name: str, location: str, capacity: int):
        self._id = warehouse_id
        self._name = name
        self._location = location
        self._capacity = capacity

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"{self._name} (ID: {self._id}) - Capacity: {self._capacity}"

    def __repr__(self) -> str:
        return f"<Warehouse: {self._id}>"