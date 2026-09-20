import pandas as pd
from typing import Optional

class ExchangeRateManager:
    def __init__(self, exchange_rates_df: pd.DataFrame):
        self.df = exchange_rates_df
        # Create a fast lookup dictionary: (rate_date, from_currency, to_currency) -> rate
        self.rates = {}
        if not self.df.empty:
            for _, row in self.df.iterrows():
                self.rates[(row['rate_date'], row['from_currency'], row['to_currency'])] = row['rate']

    def get_rate(self, rate_date: str, from_currency: str, to_currency: str) -> Optional[float]:
        if from_currency == to_currency:
            return 1.0
        
        # Exact match
        rate = self.rates.get((rate_date, from_currency, to_currency))
        if rate is not None:
            return rate
        
        # If the problem statement implies direct lookup is guaranteed when needed, we return None if missing.
        # However, let's implement cross-rate lookup through USD or EUR if necessary, but the rules strictly say:
        # \"use the row for its settlement date and the stated from_currency to to_currency direction.\"
        # This implies it should always exist directly in the file.
        return None

    def convert(self, amount: float, rate_date: str, from_currency: str, to_currency: str) -> float:
        rate = self.get_rate(rate_date, from_currency, to_currency)
        if rate is None:
            # According to rules, we must use the row for its settlement date and the stated direction.
            # If not found directly, maybe we must look for inverse? The rules explicitly say \"and the stated from_currency to to_currency direction.\"
            # Which strictly means do NOT invert.
            raise ValueError(f\"Exchange rate not found for {from_currency} -> {to_currency} on {rate_date}\")
        return amount * rate

