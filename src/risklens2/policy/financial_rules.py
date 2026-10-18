class FinancialRules:
    """Defining hard coded rules for testing. They will be ammended later for sector specific rules"""

    # profitability
    MIN_NET_MARGIN = 0.0
    MIN_REVENUE_GROWTH = -10.0
    MIN_EBITDA_MARGIN = 0.05

    # liquidity
    MIN_CURRENT_RATIO  = 1.0
    MIN_QUICK_RATIO = 0.7
    MIN_CASH_RATIO = 0.05
    MIN_WORKING_CAPITAL = 0

    # leverage
    MAX_DEBT_TO_EBITDA = 3.0
    MAX_DEBT_TO_EQUITY = 2.0
    MAX_NET_DEBT_TO_EBITDA = 3.0

    # coverage
    MIN_INTEREST_COVER = 3.0




