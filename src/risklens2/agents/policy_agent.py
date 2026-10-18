from risklens2.policy.financial_rules import FinancialRules
from risklens2.models.policy_schemas import (PolicyAssesment, PolicyRuleResult)
from risklens2.models.financials_schemas import FinancialAnalysis, ProfitabilityMetrics
from typing import Literal


financial_rules = FinancialRules()

class PolicyAgent:
    """
    This agent compares the company financials provided by FinancialAgent against the credit policy rules (defined in FinancialRules)
    """

    def evaluate(self, analysis:FinancialAnalysis):
        passed_rules = []
        failed_rules = []

        # profitability checks
        self._check_rule(
            rule_name = "EBITDA Margin",
            actual = analysis.profitability.ebitda_margin,
            threshold = financial_rules.MIN_EBITDA_MARGIN,
            comparision = "min",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        self._check_rule(
            rule_name = "Net Margin",
            actual = analysis.profitability.net_margin,
            threshold = financial_rules.MIN_NET_MARGIN,
            comparision = "min",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        self._check_rule(
            rule_name = "Revenue Growth",
            actual = analysis.profitability.revenue_growth,
            threshold = financial_rules.MIN_REVENUE_GROWTH,
            comparision = "min",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        # liquidity checks
        self._check_rule(
            rule_name = "Current Ratio",
            actual = analysis.liquidity.current_ratio,
            threshold = financial_rules.MIN_CURRENT_RATIO,
            comparision = "min",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        self._check_rule(
            rule_name = "Quick Ratio",
            actual = analysis.liquidity.quick_ratio,
            threshold = financial_rules.MIN_QUICK_RATIO,
            comparision = "min",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        self._check_rule(
            rule_name = "Working Capital",
            actual = analysis.liquidity.working_capital,
            threshold = financial_rules.MIN_WORKING_CAPITAL,
            comparision = "min",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        self._check_rule(
            rule_name = "Cash Ratio",
            actual = analysis.liquidity.cash_ratio,
            threshold = financial_rules.MIN_CASH_RATIO,
            comparision = "min",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        # leverage checks
        self._check_rule(
            rule_name = "Debt to EBITDA",
            actual = analysis.leverage.debt_to_ebitda,
            threshold = financial_rules.MAX_DEBT_TO_EBITDA,
            comparision = "max",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        self._check_rule(
            rule_name = "Debt to Equity",
            actual = analysis.leverage.debt_to_equity,
            threshold = financial_rules.MAX_DEBT_TO_EQUITY,
            comparision = "max",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        self._check_rule(
            rule_name = "Net Debt to EBITDA",
            actual = analysis.leverage.net_debt_to_ebitda,
            threshold = financial_rules.MAX_NET_DEBT_TO_EBITDA,
            comparision = "max",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        # coverage checks
        self._check_rule(
            rule_name = "Interest Cover",
            actual = analysis.coverage.interest_cover,
            threshold = financial_rules.MIN_INTEREST_COVER,
            comparision = "min",
            passed_rules = passed_rules,
            failed_rules = failed_rules
        )

        failed_count = len(failed_rules)
        recomendation = self._get_recomendation(failed_count)

        return PolicyAssesment(
            passed_rules = passed_rules,
            failed_rules = failed_rules,
            recomendation= recomendation
        )

    def _check_rule(self, rule_name, actual, threshold, comparision, passed_rules, failed_rules):
        passed = False
        if comparision == "min":
            if actual >= threshold:
                passed = True
        elif comparision == "max":
            if actual <= threshold:
                passed = True     

        result = PolicyRuleResult(
            rule_name = rule_name,
            status = "pass" if passed else "fail",
            message = f"{rule_name} passed" if passed else f"{rule_name} failed"
        )

        if passed:
            passed_rules.append(result)
        else:
            failed_rules.append(result)


    def _get_recomendation(self, failed_count: int):
        if failed_count == 0:
            return "APPROVE"
        elif failed_count <= 2:
            return "REFER"     
        else:
            return "DECLINE"

