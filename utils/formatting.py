"""
Currency & Number Formatting Utilities
======================================

Helper routines for formatting monetary values with ISO-4217 currency prefixes.
"""


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a numeric amount as a standardized ISO-4217 currency string."""
    return f"{currency} {float(amount):,.2f}"