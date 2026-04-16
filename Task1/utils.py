# utils.py
import hashlib
from datetime import datetime
from typing import Optional


class Utils:
    """Utility class containing static methods for common operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Return SHA-256 hash of the password."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def validate_item_id(item_id: str) -> bool:
        """Validate item ID format (example: must be non-empty and start with I)."""
        return bool(item_id and item_id.strip() and item_id.startswith('I'))

    @staticmethod
    def validate_quantity(qty: int) -> bool:
        """Check if quantity is a non-negative integer."""
        return isinstance(qty, int) and qty >= 0

    @staticmethod
    def generate_transaction_id(prefix: str = "T") -> str:
        """Generate a unique transaction ID using current timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        return f"{prefix}{timestamp}"

    @staticmethod
    def format_currency(amount: float) -> str:
        """Format a float as currency string."""
        return f"${amount:,.2f}"

    @staticmethod
    def parse_int(value: str, default: Optional[int] = None) -> Optional[int]:
        """Safely parse string to int, returning default on failure."""
        try:
            return int(value.strip())
        except (ValueError, AttributeError):
            return default

    @staticmethod
    def parse_float(value: str, default: Optional[float] = None) -> Optional[float]:
        """Safely parse string to float."""
        try:
            return float(value.strip())
        except (ValueError, AttributeError):
            return default