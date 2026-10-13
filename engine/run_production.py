"""
AURELIS Batch Simulation CLI
============================

Executes the deterministic financial engine across the full local dataset and
exports structured affordability decisions to `dataset/output.csv`.
"""

from datetime import datetime
import os
import sys
import time
import pandas as pd
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from data_processor import DataProcessor
from evaluator import Evaluator
from exchange_rates import ExchangeRateManager
from finance import Event, FinancialState
from llm_client import LLMClient


def run_full(data_dir: str = "dataset") -> None:
    """Execute batch affordability evaluation across all requests in `data_dir`."""
    events_df = pd.read_csv(os.path.join(data_dir, "financial_events.csv"))
    profiles_df = pd.read_csv(os.path.join(data_dir, "financial_profiles.csv"))
    requests_df = pd.read_csv(os.path.join(data_dir, "requests.csv"))
    exchange_rates_df = pd.read_csv(os.path.join(data_dir, "exchange_rates.csv"))

    exchange_mgr = ExchangeRateManager(exchange_rates_df)
    llm = LLMClient()
    _processor = DataProcessor(llm, data_dir)

    output_rows = []
    start_time = time.time()

    for _, req_row in requests_df.iterrows():
        req_id = req_row["request_id"]
        user_id = req_row["user_id"]

        prof_row = profiles_df[profiles_df["user_id"] == user_id].iloc[0]
        user_events = events_df[events_df["user_id"] == user_id]

        events = [Event(r, exchange_mgr, prof_row["home_currency"]) for _, r in user_events.iterrows()]
        state = FinancialState(user_id, prof_row, events, [], exchange_mgr)

        evaluator = Evaluator(req_row, [], state)
        res = evaluator.evaluate()
        res["request_id"] = req_id
        output_rows.append(res)

    out_df = pd.DataFrame(output_rows)
    columns = [
        "request_id",
        "amount_safe_to_pay",
        "affordability_status",
        "recommended_payment_method",
        "payment_plan",
        "earliest_date_for_full_payment",
        "spending_changes_needed",
        "decision_explanation",
    ]
    out_df = out_df[columns]
    out_df.to_csv(os.path.join(data_dir, "output.csv"), index=False)

    elapsed = time.time() - start_time
    print(f"Processed {len(requests_df)} requests in {elapsed:.2f} seconds.")


if __name__ == "__main__":
    run_full()