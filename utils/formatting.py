def format_currency(amount: float, currency: str = 'USD') -> str:
    return f"{currency} {amount:,.2f}"