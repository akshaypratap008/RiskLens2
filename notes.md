Profitability:
ebitda_margin = ebitda / revenue
net_margin = net_profit / revenue

Liquidity:
current_ratio = current_assets / current_liabilities

quick_ratio = (
    current_assets - inventory
) / current_liabilities

working_capital = (
    current_assets
    - current_liabilities
)

Leverage:
debt_to_ebitda = (
    total_debt / ebitda
)

debt_to_equity = (
    total_debt / equity
)

net_debt_to_ebitda = (
    total_debt - cash
) / ebitda

Coverage:
interest_cover = (
    ebitda / interest_expense
)

--------------------------------

account filling flags:
late_accounts_count
accounts_overdue
accounts_last_filed_date

confirmation_statement_overdue
last_confirmation_statement

insolvency_flag
insolvency_events

strike_off_action
strike_off_suspended

director_change_frequency

reg_address_change_frequency
share_capital_change_count

auditor_resignation_flag

----------------------------------

Industry Research agent:
1) Industry Outlook
    - growing, stable or declining?
2) Key industry risks? - output in the form of a list
3) Macroeconomic sentivity
    - Interest rates, Inflation, Consumer spending, Energy prices etc.
    - Output shoul contain HIGH, MEDIUM or LOW
4) Regulatory Risks
    - Financial services, Healthcare, energy, food etc
    - Output should contain the risk signal HIGH, MEDIUM or LOW
5) Sector specific insolvency trends

SIC code for testing: 41201


