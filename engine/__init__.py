"""
AURELIS Deterministic Financial Engine
======================================

Core simulation, cash-flow projection, currency normalization, and multimodal
evidence extraction primitives for the AURELIS financial intelligence platform.
"""

from .data_processor import DataProcessor
from .evaluator import Evaluator, Plan
from .exceptions import AurelisException
from .exchange_rates import ExchangeRateManager
from .finance import Event, FinancialState
from .financial_metrics import (
    calculate_altman_z_score,
    calculate_cash_conversion_cycle,
    calculate_cash_runway_months,
    calculate_current_ratio,
    calculate_debt_service_coverage_ratio,
    calculate_debt_to_income_ratio,
    calculate_discretionary_spending_ratio,
    calculate_dupont_analysis,
    calculate_emergency_fund_ratio,
    calculate_liquidity_ratio,
    calculate_margin_of_safety,
    calculate_net_burn_rate,
    calculate_net_present_value,
    calculate_net_worth,
    calculate_quick_ratio,
    calculate_rule_of_72,
    calculate_savings_rate,
)
from .llm_client import LLMClient

__all__ = [
    "AurelisException",
    "DataProcessor",
    "Evaluator",
    "Event",
    "ExchangeRateManager",
    "FinancialState",
    "LLMClient",
    "Plan",
    "calculate_altman_z_score",
    "calculate_cash_conversion_cycle",
    "calculate_cash_runway_months",
    "calculate_current_ratio",
    "calculate_debt_service_coverage_ratio",
    "calculate_debt_to_income_ratio",
    "calculate_discretionary_spending_ratio",
    "calculate_dupont_analysis",
    "calculate_emergency_fund_ratio",
    "calculate_liquidity_ratio",
    "calculate_margin_of_safety",
    "calculate_net_burn_rate",
    "calculate_net_present_value",
    "calculate_net_worth",
    "calculate_quick_ratio",
    "calculate_rule_of_72",
    "calculate_savings_rate",
]

