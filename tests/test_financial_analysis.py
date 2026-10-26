import pytest
from pydantic import ValidationError


from risklens2.agents.financial_agent import FinancialAgent
from risklens2.models.financials_schemas import FinancialInput


def test_financial_analysis_1():
    "Test Calculations"
    financials = FinancialInput(
        revenue_cy=15000000,
        revenue_py=10000000,
        ebitda=1200000,
        net_profit=650000,
        cash=450000,
        current_assets=3200000,
        inventory=750000,
        current_liabilities=2200000,
        total_assets=7800000,
        total_liabilities=4800000,
        equity=3000000,
        total_debt=2500000,
        interest_expense=180000,
    )

    analysis = FinancialAgent().analyse(financials)

    assert analysis.profitability.ebitda_margin == 0.08
    assert analysis.profitability.net_margin == 0.04
    assert analysis.profitability.revenue_growth == 50.0

    assert analysis.liquidity.current_ratio == 1.45
    assert analysis.liquidity.quick_ratio == 1.11
    assert analysis.liquidity.working_capital == 1000000
    assert analysis.liquidity.cash_ratio == 0.2

    assert analysis.leverage.debt_to_ebitda == 2.08
    assert analysis.leverage.debt_to_equity == 0.83
    assert analysis.leverage.net_debt_to_ebitda == 1.71

    assert analysis.coverage.interest_cover == 6.67


def test_financial_analysis_2():
    """Test zero division"""
    financials = FinancialInput(
        revenue_cy=15000000,
        revenue_py=0,
        ebitda=1200000,
        net_profit=650000,
        cash=450000,
        current_assets=3200000,
        inventory=750000,
        current_liabilities=2200000,
        total_assets=7800000,
        total_liabilities=4800000,
        equity=3000000,
        total_debt=2500000,
        interest_expense=180000,
    )

    with pytest.raises(ZeroDivisionError):
        FinancialAgent().analyse(financials)


def test_financial_analysis_3():
    """Test negative revenue growth"""
    financials = FinancialInput(
        revenue_cy=8000000,
        revenue_py=10000000,
        ebitda=1200000,
        net_profit=650000,
        cash=450000,
        current_assets=3200000,
        inventory=750000,
        current_liabilities=2200000,
        total_assets=7800000,
        total_liabilities=4800000,
        equity=3000000,
        total_debt=2500000,
        interest_expense=180000,
    )

    analysis = FinancialAgent().analyse(financials)

    assert analysis.profitability.revenue_growth == -20.0

def test_financial_input_1():
    """Test input validation"""
    with pytest.raises(ValidationError):
        FinancialInput(
            revenue_cy=0,
            revenue_py=10000000,
            ebitda=1200000,
            net_profit=650000,
            cash=450000,
            current_assets=3200000,
            inventory=750000,
            current_liabilities=2200000,
            total_assets=7800000,
            total_liabilities=4800000,
            equity=3000000,
            total_debt=2500000,
            interest_expense=180000,
        )