from risklens2.agents.policy_agent import PolicyAgent
from src.risklens2.models.financials_schemas import CoverageMetrics, FinancialAnalysis, LeverageMetrics, LiquidityMetrics, ProfitabilityMetrics 

def test_policy_agent_approve():
    """Test - all pass"""
    analysis = FinancialAnalysis(
        profitability=ProfitabilityMetrics(
            ebitda_margin=0.08,
            net_margin=0.04,
            revenue_growth=50.0,
        ),
        liquidity=LiquidityMetrics(
            current_ratio=1.45,
            quick_ratio=1.11,
            working_capital=1000000,
            cash_ratio=0.2,
        ),
        leverage=LeverageMetrics(
            debt_to_ebitda=2.08,
            debt_to_equity=0.83,
            net_debt_to_ebitda=1.71,
        ),
        coverage=CoverageMetrics(interest_cover=6.67),
    )

    assessment = PolicyAgent().evaluate(analysis)

    assert assessment.recomendation == "APPROVE"
    assert len(assessment.passed_rules) == 11
    assert assessment.failed_rules == []
    assert all(rule.status == "pass" for rule in assessment.passed_rules)

def make_analysis(ebitda_margin=0.08, net_margin=0.04, revenue_growth=50.0):
    return FinancialAnalysis(
        profitability=ProfitabilityMetrics(
            ebitda_margin=ebitda_margin,
            net_margin=net_margin,
            revenue_growth=revenue_growth,
        ),
        liquidity=LiquidityMetrics(
            current_ratio=1.45,
            quick_ratio=1.11,
            working_capital=1000000,
            cash_ratio=0.2,
        ),
        leverage=LeverageMetrics(
            debt_to_ebitda=2.08,
            debt_to_equity=0.83,
            net_debt_to_ebitda=1.71,
        ),
        coverage=CoverageMetrics(interest_cover=6.67),
    )


def test_policy_agent_approve_one_fail():

    analysis = make_analysis(ebitda_margin=0.04)

    assessment = PolicyAgent().evaluate(analysis)

    assert assessment.recomendation == "REFER"
    assert len(assessment.failed_rules) == 1
    assert assessment.failed_rules[0].rule_name == "EBITDA Margin"
    assert assessment.failed_rules[0].status == "fail"


def test_policy_agent_declines_more_than_2_fail():
    analysis = make_analysis(
        ebitda_margin=0.04,
        net_margin=-0.01,
        revenue_growth=-20.0,
    )

    assessment = PolicyAgent().evaluate(analysis)

    assert assessment.recomendation == "DECLINE"
    assert len(assessment.failed_rules) == 3
    assert all(rule.status == "fail" for rule in assessment.failed_rules)