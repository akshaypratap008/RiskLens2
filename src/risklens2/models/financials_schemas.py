from pydantic import BaseModel, Field

class FinancialInput(BaseModel):
    revenue_cy: float = Field(..., description = "Total turnover of the company in the last financial year", gt=0)
    revenue_py: float= Field(default = None, description= "Total turnover of the company in the previous year.")
    ebitda: float = Field(description = "Earnings before tax, depreciation and amortization (EBITDA) during the last financial year")
    net_profit: float = Field(description = "Bottom line profitability after all the expenses")
    cash: float = Field(description= "Available liquidity used to meet short-term obligations.")
    current_assets: float = Field(description= "Short term assets to support daily operations and liquidity")
    inventory: float = Field(description= "Value of existing stock held by the company")
    current_liabilities : float = Field(description="Short term obligations due within the coming year")
    total_assets: float = Field(description = "Total resources controled by the company.")
    total_liabilities : float = Field(description= "Total debts and obligations owed by the business.")
    equity: float = Field(description = "Net Assets attributable to shareholders")
    total_debt: float = Field(description = "Interest bearing borrowing including the short term and long term debt")
    interest_expense: float = Field(description= "Financial cost incurred due to borrowings during the reported period.")

class ProfitabilityMetrics(BaseModel):
    ebitda_margin : float = Field(description = "Operating earnings as a percentage of revenue.")
    net_margin : float = Field(description= "Net profit as a percentage of revenue.")
    revenue_growth: float | None = Field(default = None, description = "YOY growth")

class LiquidityMetrics(BaseModel):
    current_ratio : float = Field(description= "Ability to cover short-term liabilities with current assets.")
    quick_ratio : float = Field(description="Ability to cover short-term liabilities with liquid assets.")
    working_capital: float = Field(description= "Surplus current assets available for operations.")
    cash_ratio: float = Field(description="Coverage of short-term liabilities using cash.")

class LeverageMetrics(BaseModel):
    debt_to_ebitda : float = Field(description= "Debt and EBITDA ratio. Debt burden relative to operating earnings.")
    debt_to_equity: float = Field(description = "Debt and Equity ratio. Debt relative to shareholder capital.")
    net_debt_to_ebitda: float = Field(description= "ratio of (total_debt - cash) and ebitda")

class CoverageMetrics(BaseModel):
    interest_cover : float = Field(description = "Ability to meet interest payments from earnings.")

class FinancialAnalysis(BaseModel):
    profitability : ProfitabilityMetrics
    liquidity: LiquidityMetrics
    leverage: LeverageMetrics
    coverage: CoverageMetrics


