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
]
