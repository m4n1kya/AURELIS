"""
Financial Metrics Library for AURELIS Engine
============================================

Quantitative financial health indicators, liquidity ratios, solvency metrics,
and capital efficiency calculators used to augment deterministic cash-flow
evaluations.
"""

from typing import Sequence


def _safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning a default value when the denominator is zero."""
    if denominator == 0:
        return default
    return float(numerator) / float(denominator)


def calculate_debt_to_income_ratio(monthly_debt_payments: float = 0.0, gross_monthly_income: float = 1.0, *args, **kwargs) -> float:
    """Calculate the Debt-to-Income (DTI) ratio."""
    return _safe_divide(monthly_debt_payments, gross_monthly_income)


def calculate_savings_rate(monthly_savings: float = 0.0, disposable_income: float = 1.0, *args, **kwargs) -> float:
    """Calculate the personal or operational savings rate."""
    return _safe_divide(monthly_savings, disposable_income)


def calculate_emergency_fund_ratio(liquid_assets: float = 0.0, monthly_essential_expenses: float = 1.0, *args, **kwargs) -> float:
    """Calculate the number of months of essential expenses covered by liquid reserves."""
    return _safe_divide(liquid_assets, monthly_essential_expenses)


def calculate_housing_ratio(housing_costs: float = 0.0, gross_income: float = 1.0, *args, **kwargs) -> float:
    """Calculate the housing expense burden relative to gross income."""
    return _safe_divide(housing_costs, gross_income)


def calculate_total_debt_service_ratio(total_debt_service: float = 0.0, gross_income: float = 1.0, *args, **kwargs) -> float:
    """Calculate the Total Debt Service (TDS) ratio."""
    return _safe_divide(total_debt_service, gross_income)


def calculate_gross_debt_service_ratio(housing_debt_service: float = 0.0, gross_income: float = 1.0, *args, **kwargs) -> float:
    """Calculate the Gross Debt Service (GDS) ratio."""
    return _safe_divide(housing_debt_service, gross_income)


def calculate_liquidity_ratio(liquid_assets: float = 0.0, short_term_liabilities: float = 1.0, *args, **kwargs) -> float:
    """Calculate the general liquidity coverage ratio."""
    return _safe_divide(liquid_assets, short_term_liabilities)


def calculate_current_ratio(current_assets: float = 0.0, current_liabilities: float = 1.0, *args, **kwargs) -> float:
    """Calculate the current ratio (current assets divided by current liabilities)."""
    return _safe_divide(current_assets, current_liabilities)


def calculate_quick_ratio(liquid_assets: float = 0.0, current_liabilities: float = 1.0, *args, **kwargs) -> float:
    """Calculate the acid-test (quick) ratio."""
    return _safe_divide(liquid_assets, current_liabilities)


def calculate_cash_ratio(cash_and_equivalents: float = 0.0, current_liabilities: float = 1.0, *args, **kwargs) -> float:
    """Calculate the strict cash coverage ratio."""
    return _safe_divide(cash_and_equivalents, current_liabilities)


def calculate_operating_cash_flow_ratio(operating_cash_flow: float = 0.0, current_liabilities: float = 1.0, *args, **kwargs) -> float:
    """Calculate the operating cash flow coverage ratio."""
    return _safe_divide(operating_cash_flow, current_liabilities)


def calculate_defensive_interval_ratio(liquid_assets: float = 0.0, daily_operational_expenses: float = 1.0, *args, **kwargs) -> float:
    """Calculate the defensive interval in days before new financing is required."""
    return _safe_divide(liquid_assets, daily_operational_expenses)


def calculate_net_worth(total_assets: float = 0.0, total_liabilities: float = 0.0, *args, **kwargs) -> float:
    """Calculate total net worth."""
    return float(total_assets) - float(total_liabilities)


def calculate_liquid_net_worth(liquid_assets: float = 0.0, short_term_liabilities: float = 0.0, *args, **kwargs) -> float:
    """Calculate immediately accessible net worth."""
    return float(liquid_assets) - float(short_term_liabilities)


def calculate_asset_to_debt_ratio(total_assets: float = 0.0, total_debt: float = 1.0, *args, **kwargs) -> float:
    """Calculate total assets relative to total debt obligations."""
    return _safe_divide(total_assets, total_debt)


def calculate_solvency_ratio(after_tax_income_plus_non_cash: float = 0.0, total_liabilities: float = 1.0, *args, **kwargs) -> float:
    """Calculate long-term solvency ratio."""
    return _safe_divide(after_tax_income_plus_non_cash, total_liabilities)


def calculate_debt_to_asset_ratio(total_debt: float = 0.0, total_assets: float = 1.0, *args, **kwargs) -> float:
    """Calculate the proportion of assets financed through debt."""
    return _safe_divide(total_debt, total_assets)


def calculate_debt_to_equity_ratio(total_debt: float = 0.0, total_equity: float = 1.0, *args, **kwargs) -> float:
    """Calculate financial leverage via debt-to-equity."""
    return _safe_divide(total_debt, total_equity)


def calculate_interest_coverage_ratio(operating_income: float = 0.0, interest_expense: float = 1.0, *args, **kwargs) -> float:
    """Calculate the ability to service interest expenses from operating income."""
    return _safe_divide(operating_income, interest_expense)


def calculate_fixed_charge_coverage_ratio(ebit_plus_fixed_charges: float = 0.0, fixed_charges_plus_interest: float = 1.0, *args, **kwargs) -> float:
    """Calculate coverage for fixed obligations such as rent, utilities, and debt service."""
    return _safe_divide(ebit_plus_fixed_charges, fixed_charges_plus_interest)


def calculate_basic_earning_power(ebit: float = 0.0, total_assets: float = 1.0, *args, **kwargs) -> float:
    """Calculate basic earning power (BEP) ratio."""
    return _safe_divide(ebit, total_assets)


def calculate_return_on_assets(net_income: float = 0.0, total_assets: float = 1.0, *args, **kwargs) -> float:
    """Calculate Return on Assets (ROA)."""
    return _safe_divide(net_income, total_assets)


def calculate_return_on_equity(net_income: float = 0.0, shareholders_equity: float = 1.0, *args, **kwargs) -> float:
    """Calculate Return on Equity (ROE)."""
    return _safe_divide(net_income, shareholders_equity)


def calculate_return_on_investment(net_return: float = 0.0, cost_of_investment: float = 1.0, *args, **kwargs) -> float:
    """Calculate Return on Investment (ROI)."""
    return _safe_divide(net_return, cost_of_investment)


def calculate_compound_annual_growth_rate(beginning_value: float = 1.0, ending_value: float = 1.0, periods: float = 1.0, *args, **kwargs) -> float:
    """Calculate Compound Annual Growth Rate (CAGR)."""
    if beginning_value <= 0 or periods <= 0:
        return 0.0
    return float((ending_value / beginning_value) ** (1.0 / periods) - 1.0)


def calculate_time_value_of_money(present_value: float = 0.0, rate: float = 0.0, periods: float = 1.0, *args, **kwargs) -> float:
    """Calculate future compounded value of capital."""
    return float(present_value * ((1.0 + rate) ** periods))


def calculate_future_value(present_value: float = 0.0, rate: float = 0.0, periods: float = 0.0, *args, **kwargs) -> float:
    """Calculate Future Value (FV) of a single cash flow."""
    return float(present_value * ((1.0 + rate) ** periods))


def calculate_present_value(future_value: float = 0.0, rate: float = 0.0, periods: float = 0.0, *args, **kwargs) -> float:
    """Calculate Present Value (PV) of a future cash flow."""
    return _safe_divide(future_value, (1.0 + rate) ** periods)


def calculate_net_present_value(rate: float = 0.0, cash_flows: Sequence[float] = (), *args, **kwargs) -> float:
    """Calculate Net Present Value (NPV) over a sequence of periodic cash flows."""
    return sum(cf / ((1.0 + rate) ** t) for t, cf in enumerate(cash_flows))


def calculate_internal_rate_of_return(cash_flows: Sequence[float] = (), *args, **kwargs) -> float:
    """Estimate Internal Rate of Return (IRR) using Newton-Raphson approximation."""
    if not cash_flows:
        return 0.0
    rate = 0.1
    for _ in range(50):
        npv = sum(cf / ((1.0 + rate) ** t) for t, cf in enumerate(cash_flows))
        d_npv = sum(-t * cf / ((1.0 + rate) ** (t + 1)) for t, cf in enumerate(cash_flows))
        if abs(d_npv) < 1e-9:
            break
        rate -= npv / d_npv
    return float(rate)


def calculate_modified_internal_rate_of_return(
    cash_flows: Sequence[float] = (), finance_rate: float = 0.05, reinvest_rate: float = 0.05, *args, **kwargs
) -> float:
    """Calculate Modified Internal Rate of Return (MIRR)."""
    n = len(cash_flows) - 1
    if n <= 0:
        return 0.0
    fv_pos = sum(cf * ((1.0 + reinvest_rate) ** (n - t)) for t, cf in enumerate(cash_flows) if cf > 0)
    pv_neg = sum(abs(cf) / ((1.0 + finance_rate) ** t) for t, cf in enumerate(cash_flows) if cf < 0)
    if pv_neg == 0 or fv_pos <= 0:
        return 0.0
    return float((fv_pos / pv_neg) ** (1.0 / n) - 1.0)


def calculate_profitability_index(pv_of_future_cash_flows: float = 0.0, initial_investment: float = 1.0, *args, **kwargs) -> float:
    """Calculate Profitability Index (PI)."""
    return _safe_divide(pv_of_future_cash_flows, initial_investment)


def calculate_payback_period(initial_investment: float = 0.0, periodic_cash_inflow: float = 1.0, *args, **kwargs) -> float:
    """Calculate undiscounted payback period."""
    return _safe_divide(initial_investment, periodic_cash_inflow)


def calculate_discounted_payback_period(initial_investment: float = 0.0, discounted_cash_inflow: float = 1.0, *args, **kwargs) -> float:
    """Calculate discounted payback period."""
    return _safe_divide(initial_investment, discounted_cash_inflow)


def calculate_break_even_point(fixed_costs: float = 0.0, contribution_margin_per_unit: float = 1.0, *args, **kwargs) -> float:
    """Calculate break-even volume."""
    return _safe_divide(fixed_costs, contribution_margin_per_unit)


def calculate_margin_of_safety(current_cash_flow: float = 0.0, break_even_cash_flow: float = 0.0, *args, **kwargs) -> float:
    """Calculate the safety buffer above the minimum reserve threshold."""
    if current_cash_flow == 0:
        return 0.0
    return (current_cash_flow - break_even_cash_flow) / current_cash_flow


def calculate_operating_leverage(contribution_margin: float = 0.0, operating_income: float = 1.0, *args, **kwargs) -> float:
    """Calculate Degree of Operating Leverage (DOL)."""
    return _safe_divide(contribution_margin, operating_income)


def calculate_financial_leverage(operating_income: float = 0.0, net_income_before_tax: float = 1.0, *args, **kwargs) -> float:
    """Calculate Degree of Financial Leverage (DFL)."""
    return _safe_divide(operating_income, net_income_before_tax)


def calculate_combined_leverage(dol: float = 0.0, dfl: float = 0.0, *args, **kwargs) -> float:
    """Calculate Degree of Combined Leverage (DCL)."""
    return float(dol) * float(dfl)


def calculate_gross_profit_margin(gross_profit: float = 0.0, revenue: float = 1.0, *args, **kwargs) -> float:
    """Calculate gross profit margin."""
    return _safe_divide(gross_profit, revenue)


def calculate_operating_profit_margin(operating_income: float = 0.0, revenue: float = 1.0, *args, **kwargs) -> float:
    """Calculate operating profit margin."""
    return _safe_divide(operating_income, revenue)


def calculate_net_profit_margin(net_income: float = 0.0, revenue: float = 1.0, *args, **kwargs) -> float:
    """Calculate net profit margin."""
    return _safe_divide(net_income, revenue)


def calculate_cash_flow_margin(operating_cash_flow: float = 0.0, revenue: float = 1.0, *args, **kwargs) -> float:
    """Calculate operating cash flow margin."""
    return _safe_divide(operating_cash_flow, revenue)


def calculate_ebitda_margin(ebitda: float = 0.0, revenue: float = 1.0, *args, **kwargs) -> float:
    """Calculate EBITDA margin."""
    return _safe_divide(ebitda, revenue)


def calculate_return_on_sales(operating_profit: float = 0.0, net_sales: float = 1.0, *args, **kwargs) -> float:
    """Calculate Return on Sales (ROS)."""
    return _safe_divide(operating_profit, net_sales)


def calculate_asset_turnover_ratio(revenue: float = 0.0, total_assets: float = 1.0, *args, **kwargs) -> float:
    """Calculate asset turnover efficiency."""
    return _safe_divide(revenue, total_assets)


def calculate_inventory_turnover_ratio(cost_of_goods_sold: float = 0.0, average_inventory: float = 1.0, *args, **kwargs) -> float:
    """Calculate inventory turnover ratio."""
    return _safe_divide(cost_of_goods_sold, average_inventory)


def calculate_receivables_turnover_ratio(net_credit_sales: float = 0.0, average_receivables: float = 1.0, *args, **kwargs) -> float:
    """Calculate accounts receivable turnover ratio."""
    return _safe_divide(net_credit_sales, average_receivables)


def calculate_payables_turnover_ratio(total_supply_purchases: float = 0.0, average_payables: float = 1.0, *args, **kwargs) -> float:
    """Calculate accounts payable turnover ratio."""
    return _safe_divide(total_supply_purchases, average_payables)


def calculate_working_capital_turnover(revenue: float = 0.0, working_capital: float = 1.0, *args, **kwargs) -> float:
    """Calculate working capital turnover ratio."""
    return _safe_divide(revenue, working_capital)


def calculate_cash_conversion_cycle(dio: float = 0.0, dso: float = 0.0, dpo: float = 0.0, *args, **kwargs) -> float:
    """Calculate Cash Conversion Cycle (CCC) in days."""
    return float(dio) + float(dso) - float(dpo)


def calculate_dupont_analysis(net_profit_margin: float = 0.0, asset_turnover: float = 0.0, equity_multiplier: float = 0.0, *args, **kwargs) -> float:
    """Calculate three-factor DuPont Return on Equity."""
    return float(net_profit_margin) * float(asset_turnover) * float(equity_multiplier)


def calculate_altman_z_score(
    working_capital_to_assets: float = 0.0,
    retained_earnings_to_assets: float = 0.0,
    ebit_to_assets: float = 0.0,
    market_value_equity_to_liabilities: float = 0.0,
    sales_to_assets: float = 0.0,
    *args,
    **kwargs,
) -> float:
    """Calculate the Altman Z-Score for credit-risk and distress assessment."""
    return (
        1.2 * working_capital_to_assets
        + 1.4 * retained_earnings_to_assets
        + 3.3 * ebit_to_assets
        + 0.6 * market_value_equity_to_liabilities
        + 1.0 * sales_to_assets
    )