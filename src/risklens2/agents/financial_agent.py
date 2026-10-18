from risklens2.models.financials_schemas import FinancialInput, FinancialAnalysis, ProfitabilityMetrics, LiquidityMetrics, LeverageMetrics, CoverageMetrics

class FinancialAgent:
    """
    This agents takes the Company financials data and calculates and analyses the important ratios. 
    FinancialInput is either provided by the user or extracted programatically. 
    """

    def analyse(self, financials: FinancialInput) -> FinancialAnalysis:
        """Calculate all the financial metrics from the FinancialInput given.
        """
        profitability = self._calculate_profitability(financials)
        liquidity = self._calculate_liquidity(financials)
        leverage = self._calculate_leverage(financials)
        coverage = self._calculate_coverage(financials)

        return FinancialAnalysis(
            profitability=profitability,
            liquidity=liquidity,
            leverage=leverage,
            coverage=coverage
        )

    def _calculate_profitability(self, financials:FinancialInput) -> ProfitabilityMetrics:
        """Calculate metrics related to Profitability"""
        ebitda_margin = financials.ebitda / financials.revenue_cy
        net_margin = financials.net_profit / financials.revenue_cy
        revenue_growth = 100 * ((financials.revenue_cy - financials.revenue_py) / financials.revenue_py)
        return ProfitabilityMetrics(
            ebitda_margin=round(ebitda_margin, 2),
            net_margin=round(net_margin, 2),
            revenue_growth=round(revenue_growth, 2)
        )

    def _calculate_liquidity(self, financials:FinancialInput) -> LiquidityMetrics:
        """Calculates metrics related to Liquidity"""
        current_ratio = financials.current_assets / financials.current_liabilities
        quick_ratio = (financials.current_assets - financials.inventory) / financials.current_liabilities
        working_capital = financials.current_assets - financials.current_liabilities
        cash_ratio = financials.cash / financials.current_liabilities
        return LiquidityMetrics(
            current_ratio=round(current_ratio, 2),
            quick_ratio=round(quick_ratio, 2),
            working_capital=round(working_capital, 2),
            cash_ratio=round(cash_ratio, 2)
        )

    def _calculate_leverage(self, financials: FinancialInput) -> LeverageMetrics:
        """Calculates metrics related to Leverage"""
        debt_to_ebitda = financials.total_debt / financials.ebitda
        debt_to_equity = financials.total_debt / financials.equity
        net_debt_to_ebitda = (financials.total_debt - financials.cash)/financials.ebitda
        return LeverageMetrics(
            debt_to_ebitda=round(debt_to_ebitda, 2),
            debt_to_equity=round(debt_to_equity, 2),
            net_debt_to_ebitda=round(net_debt_to_ebitda, 2)
        )

    def _calculate_coverage(self, financials: FinancialInput) -> CoverageMetrics:
        """Calculates metrics related to coverage"""
        interest_cover = financials.ebitda / financials.interest_expense
        return CoverageMetrics(
            interest_cover=round(interest_cover, 2)
        )
