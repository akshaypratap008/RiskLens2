from pydantic import BaseModel, Field

class FinancialInput(BaseModel):
    revenue: float = Field(
        ..., description = "Total turnover of the company in the last financial year", gt=0
    )
    ebitda: float = Field(
        description = "Earnings before tax, depreciation and amortization (EBITDA) during the last financial year"
    )
    net_profit: float = Field(
        description = "Bottom line profitability after all the expenses"
    )
    cash: float = Field(
        description= "CAvailable liquidity used to meet short-term obligations."
    )
    current_assets: float = Field(
        description= "Short term assets to support daily operations and liquidity"
    )
    inventory: float = Field(
        description= "Value of existing stock held by the company"
    )
    current_liabilities : float = Field(
        description="Short term obligations due within the coming year"
    )
    total_assets: float = Field(
        description = "Total resources controled by the company."
    )
    total_liabilities : float = Field(
        description= "Total debts and obligations owed by the business."
    )
    equity: float = Field(
        description = "Net Assets attributable to shareholders"
    )
    total_debt: float = Field(
        description = "Interest bearing borrowing including the short term and long term debt"
    )
    interest_expense: float = Field(
        description= "Financial cost incurred due to borrowings during the reported period."
    )

class ProfitabilityMetrics(BaseModel):
    ebitda_margin : float
    net_margin : float
    revenue_growth: float | None

class LiquidityMetrics(BaseModel):


class FinancialAnalysis(BaseModel):
    profitability : ProfitabilityMetrics
