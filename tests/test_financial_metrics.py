"""
Unit Tests for Quantitative Financial Metrics Library
=====================================================

Validates liquidity, solvency, capital efficiency, profitability,
and investment valuation calculations, including zero-division guards.
"""

import pytest
from engine.financial_metrics import (
    calculate_altman_z_score,
    calculate_asset_turnover_ratio,
    calculate_cash_conversion_cycle,
    calculate_cash_ratio,
    calculate_cash_runway_months,
    calculate_compound_annual_growth_rate,
    calculate_current_ratio,
    calculate_debt_service_coverage_ratio,
    calculate_debt_to_equity_ratio,
    calculate_debt_to_income_ratio,
    calculate_discretionary_spending_ratio,
    calculate_dupont_analysis,
    calculate_emergency_fund_ratio,
    calculate_future_value,
    calculate_gross_profit_margin,
    calculate_interest_coverage_ratio,
    calculate_internal_rate_of_return,
    calculate_liquidity_ratio,
    calculate_margin_of_safety,
    calculate_net_burn_rate,
    calculate_net_present_value,
    calculate_net_profit_margin,
    calculate_net_worth,
    calculate_operating_cash_flow_ratio,
    calculate_payback_period,
    calculate_present_value,
    calculate_profitability_index,
    calculate_quick_ratio,
    calculate_return_on_assets,
    calculate_return_on_equity,
    calculate_return_on_investment,
    calculate_rule_of_72,
    calculate_savings_rate,
    calculate_solvency_ratio,
)


class TestLiquidityRatios:
    def test_current_ratio(self):
        assert calculate_current_ratio(current_assets=2000.0, current_liabilities=1000.0) == 2.0
        assert calculate_current_ratio(current_assets=500.0, current_liabilities=0.0) == 0.0

    def test_quick_ratio(self):
        assert calculate_quick_ratio(liquid_assets=1500.0, current_liabilities=1000.0) == 1.5

    def test_cash_ratio(self):
        assert calculate_cash_ratio(cash_and_equivalents=800.0, current_liabilities=1000.0) == 0.8

    def test_emergency_fund_ratio(self):
        assert calculate_emergency_fund_ratio(liquid_assets=18000.0, monthly_essential_expenses=3000.0) == 6.0


class TestSolvencyAndDebtRatios:
    def test_debt_to_income_ratio(self):
        assert calculate_debt_to_income_ratio(monthly_debt_payments=1500.0, gross_monthly_income=5000.0) == 0.3

    def test_debt_to_equity_ratio(self):
        assert calculate_debt_to_equity_ratio(total_debt=40000.0, total_equity=80000.0) == 0.5

    def test_interest_coverage_ratio(self):
        assert calculate_interest_coverage_ratio(operating_income=50000.0, interest_expense=10000.0) == 5.0

    def test_net_worth(self):
        assert calculate_net_worth(total_assets=250000.0, total_liabilities=100000.0) == 150000.0


class TestProfitabilityAndEfficiency:
    def test_margins(self):
        assert calculate_gross_profit_margin(gross_profit=40000.0, revenue=100000.0) == 0.4
        assert calculate_net_profit_margin(net_income=15000.0, revenue=100000.0) == 0.15

    def test_returns(self):
        assert calculate_return_on_assets(net_income=10000.0, total_assets=100000.0) == 0.1
        assert calculate_return_on_equity(net_income=15000.0, shareholders_equity=50000.0) == 0.3
        assert calculate_return_on_investment(net_return=2500.0, cost_of_investment=10000.0) == 0.25

    def test_dupont_analysis(self):
        # ROE = Net Profit Margin * Asset Turnover * Equity Multiplier
        roe = calculate_dupont_analysis(net_profit_margin=0.1, asset_turnover=1.5, equity_multiplier=2.0)
        assert pytest.approx(roe) == 0.3

    def test_cash_conversion_cycle(self):
        # CCC = DIO + DSO - DPO
        ccc = calculate_cash_conversion_cycle(dio=45.0, dso=30.0, dpo=35.0)
        assert ccc == 40.0


class TestValuationAndCashFlow:
    def test_future_and_present_value(self):
        fv = calculate_future_value(present_value=1000.0, rate=0.05, periods=2.0)
        assert pytest.approx(fv) == 1102.5
        pv = calculate_present_value(future_value=1102.5, rate=0.05, periods=2.0)
        assert pytest.approx(pv) == 1000.0

    def test_cagr(self):
        cagr = calculate_compound_annual_growth_rate(beginning_value=100.0, ending_value=144.0, periods=2.0)
        assert pytest.approx(cagr) == 0.2

    def test_net_present_value(self):
        cash_flows = [-1000.0, 300.0, 400.0, 500.0]
        npv = calculate_net_present_value(rate=0.1, cash_flows=cash_flows)
        # -1000 + 300/1.1 + 400/1.21 + 500/1.331 = -1000 + 272.727 + 330.578 + 375.657 = -21.037
        assert pytest.approx(npv, rel=1e-2) == -21.04

    def test_altman_z_score(self):
        z = calculate_altman_z_score(
            working_capital_to_assets=0.2,
            retained_earnings_to_assets=0.3,
            ebit_to_assets=0.15,
            market_value_equity_to_liabilities=0.8,
            sales_to_assets=1.2,
        )
        # 1.2*0.2 + 1.4*0.3 + 3.3*0.15 + 0.6*0.8 + 1.0*1.2 = 0.24 + 0.42 + 0.495 + 0.48 + 1.2 = 2.835
        assert pytest.approx(z) == 2.835


class TestPersonalCashFlowAndRunwayMetrics:
    def test_net_burn_rate(self):
        # Inflows 3000, Outflows 4500 -> Burn rate 1500
        assert calculate_net_burn_rate(cash_inflows=3000.0, cash_outflows=4500.0) == 1500.0
        # Positive cash flow: Inflows 5000, Outflows 3000 -> Burn rate 0
        assert calculate_net_burn_rate(cash_inflows=5000.0, cash_outflows=3000.0) == 0.0
        # Flat cash flow
        assert calculate_net_burn_rate(cash_inflows=2000.0, cash_outflows=2000.0) == 0.0

    def test_cash_runway_months(self):
        # 12000 liquid reserves with 2000 monthly burn -> 6 months runway
        assert calculate_cash_runway_months(current_liquid_reserves=12000.0, monthly_burn_rate=2000.0) == 6.0
        # 0 or negative burn rate (positive cash flow) -> infinite runway
        assert calculate_cash_runway_months(current_liquid_reserves=10000.0, monthly_burn_rate=0.0) == float("inf")
        assert calculate_cash_runway_months(current_liquid_reserves=10000.0, monthly_burn_rate=-500.0) == float("inf")

    def test_debt_service_coverage_ratio(self):
        # 6000 net operating income, 2000 debt service -> DSCR 3.0
        assert calculate_debt_service_coverage_ratio(net_operating_income=6000.0, total_debt_service=2000.0) == 3.0
        # Zero debt service guard
        assert calculate_debt_service_coverage_ratio(net_operating_income=6000.0, total_debt_service=0.0) == 0.0

    def test_discretionary_spending_ratio(self):
        # 800 discretionary out of 4000 total expenditures -> 0.20
        assert calculate_discretionary_spending_ratio(discretionary_expenses=800.0, total_expenses=4000.0) == 0.2
        # Zero total expenditures guard
        assert calculate_discretionary_spending_ratio(discretionary_expenses=500.0, total_expenses=0.0) == 0.0

    def test_rule_of_72(self):
        # At 8% annual return, capital doubles in ~9 years
        assert calculate_rule_of_72(annual_rate_of_return=8.0) == 9.0
        # At 6% return, ~12 years
        assert calculate_rule_of_72(annual_rate_of_return=6.0) == 12.0
        # Zero / negative return guard
        assert calculate_rule_of_72(annual_rate_of_return=0.0) == 0.0
        assert calculate_rule_of_72(annual_rate_of_return=-4.0) == 0.0

