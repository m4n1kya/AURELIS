"""
Multi-Currency Exchange Rate Manager
====================================

Provides deterministic spot-rate lookups and currency conversions across
settlement dates for normalizing foreign-denominated cash-flow events into a
user's home currency.
"""

from typing import Dict, Optional, Tuple
import pandas as pd


class ExchangeRateManager:
    """Manages historical and forward spot exchange rates indexed by date and currency pair."""

    def __init__(self, exchange_rates_df: pd.DataFrame):
        self.df = exchange_rates_df
        self.rates: Dict[Tuple[str, str, str], float] = {}
        if not self.df.empty:
            for _, row in self.df.iterrows():
                key = (str(row["rate_date"]), str(row["from_currency"]), str(row["to_currency"]))
                self.rates[key] = float(row["rate"])

    def get_rate(self, rate_date: str, from_currency: str, to_currency: str) -> Optional[float]:
        """Return the spot conversion rate for a given date and directional currency pair."""
        if from_currency == to_currency:
            return 1.0
        return self.rates.get((rate_date, from_currency, to_currency))

    def convert(self, amount: float, rate_date: str, from_currency: str, to_currency: str) -> float:
        """Convert an amount from source currency to target currency on the specified settlement date."""
        rate = self.get_rate(rate_date, from_currency, to_currency)
        if rate is None:
            raise ValueError(f"Exchange rate not found for {from_currency} -> {to_currency} on {rate_date}")
        return float(amount) * rate
