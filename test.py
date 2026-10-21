from src.risklens2.agents.financial_agent import FinancialAgent
from risklens2.models.financials_schemas import FinancialInput
from risklens2.agents.policy_agent import PolicyAgent
from risklens2.agents.memo_agent import MemoAgent
from risklens2.agents.company_research_agent import CompanyResearchAgent
from src.risklens2.utils import load_prompt

import json
from pathlib import Path

# sample_company_data_path = Path("tests/sample_company.json")

# with open(sample_company_data_path, "rb") as file:
#     sample_test_json = json.load(file)

# financial_agent = FinancialAgent()
# policy_agent = PolicyAgent()
# memo_agent = MemoAgent()

# for company in sample_test_json['companies']:
#     company_profile = {"name": company}
#     financials = FinancialInput.model_validate(company['financials'])

#     print(company['company_name'])
#     financial_analysis_results = financial_agent.analyse(financials=financials)
#     policy_assesement = policy_agent.evaluate(analysis = financial_analysis_results)
#     memo = memo_agent.create_memo(
#         company_profile=company_profile,
#         financial_analysis=financial_analysis_results,
#         policy_assesment=policy_assesement,
#         industry_analysis= {},
#         media_analysis= {}
#     )
    
#     print("-------MEMO----------")
#     print(memo)
#     print()


COMPANY_NUMBER = "04458620"

research_agent = CompanyResearchAgent()

filings_details = research_agent.get_filings_details(COMPANY_NUMBER)
print(filings_details)
    

