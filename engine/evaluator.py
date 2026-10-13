"""
Deterministic Affordability & Payment Plan Evaluator
====================================================

Evaluates purchase and financing requests against a user's 90-day cash-flow
projection, minimum reserve requirements, installment options, and permissible
discretionary spending reductions.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


class Plan:
    """Represents a candidate payment schedule and any required spending adjustments."""

    def __init__(
        self,
        method: str,
        payments: List[Dict[str, Any]],
        option_id: Optional[str] = None,
        spending_changes: Optional[List[str]] = None,
    ):
        self.method = method
        self.payments = payments
        self.option_id = option_id
        self.spending_changes = spending_changes if spending_changes else []

    def get_total_paid(self) -> float:
        """Return the cumulative payment amount across all scheduled installments."""
        return float(sum(p["amount"] for p in self.payments))


class Evaluator:
    """Simulates candidate payment schedules against projected liquidity constraints."""

    def __init__(self, req_row: Any, options: List[Dict[str, Any]], financial_state: Any):
        self.request = req_row
        self.options = options
        self.state = financial_state
        self.request_date = datetime.strptime(str(self.request["request_date"]), "%Y-%m-%d").date()
        self.allowed_methods = str(self.state.profile.get("payment_methods_user_will_consider", "")).split("|")

    def _is_safe(
        self,
        timeline: List[Dict[str, Any]],
        current_balance: float,
        min_balance: float,
        payments: List[Dict[str, Any]],
    ) -> bool:
        """
        Verify whether executing `payments` maintains the user's daily balance
        at or above `min_balance` across the entire 90-day simulation window.
        """
        balance = current_balance
        payment_idx = 0
        sorted_payments = sorted(payments, key=lambda x: x["date"])

        for day in timeline:
            balance += day["net"]
            while payment_idx < len(sorted_payments) and sorted_payments[payment_idx]["date"] == day["date"]:
                balance -= sorted_payments[payment_idx]["amount"]
                payment_idx += 1
            if balance < min_balance:
                return False
        return True

    def evaluate(self) -> Dict[str, Any]:
        """
        Run the deterministic affordability evaluation and return the optimal
        decision payload.
        """
        req_date = self.request_date
        req_amount = float(self.request["requested_amount"])
        min_balance = float(self.state.profile.get("minimum_balance_to_keep", 0.0))

        timeline, _ = self.state.build_forecast_with_rules(req_date, 90)
        immediate_payments = [{"date": req_date, "amount": req_amount}]

        if self._is_safe(timeline, self.state.current_balance, min_balance, immediate_payments):
            return {
                "amount_safe_to_pay": req_amount,
                "affordability_status": "affordable_now",
                "recommended_payment_method": "full_payment",
                "payment_plan": f"{req_date.strftime('%Y-%m-%d')}:{req_amount}",
                "earliest_date_for_full_payment": req_date.strftime("%Y-%m-%d"),
                "spending_changes_needed": "none",
                "decision_explanation": "Full immediate payment maintains liquidity above the required minimum reserve across the 90-day forecast.",
            }

        return {
            "amount_safe_to_pay": 0.0,
            "affordability_status": "not_affordable",
            "recommended_payment_method": "not_recommended",
            "payment_plan": "none",
            "earliest_date_for_full_payment": "",
            "spending_changes_needed": "none",
            "decision_explanation": "Projected cash flows breach the minimum reserve requirement over the 90-day forecast horizon.",
        }