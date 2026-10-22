from src.risklens2.agents.financial_agent import FinancialAgent
from risklens2.models.financials_schemas import FinancialInput
from risklens2.agents.policy_agent import PolicyAgent
from risklens2.agents.memo_agent import MemoAgent
from risklens2.agents.company_research_agent import CompanyResearchAgent
from risklens2.agents.media_agent import MediaAgent
from src.risklens2.utils import load_prompt

import json
from pathlib import Path

COMPANY_NUMBER = "SC226769"

# sample_company_data_path = Path("tests/sample_company.json")

# with open(sample_company_data_path, "rb") as file:
#     sample_test_json = json.load(file)

# company = sample_test_json['companies'][0]

# financials = FinancialInput.model_validate(company['financials'])
# financial_agent = FinancialAgent()
# financial_analysis = financial_agent.analyse(financials)


# policy_agent = PolicyAgent()
# policy_assesment = policy_agent.evaluate(financial_analysis)


# research_agent = CompanyResearchAgent()
# company_research = research_agent.research(COMPANY_NUMBER)

# memo_agent = MemoAgent()
# memo = memo_agent.create_memo(
#     company_profile=financials,
#     financial_analysis=financial_analysis,
#     policy_assesment=policy_assesment,
#     industry_analysis=None,
#     media_analysis=None,
#     company_research=company_research
# )

# print(financials)
# print("**************************************************\n")

# print(financial_analysis)
# print("**************************************************\n")

# print(policy_assesment)
# print("**************************************************\n")

# print(company_research)
# print("**************************************************\n")

# print("----MEMO----")
# print(memo)

media_agent = MediaAgent(company_name="PATISSERIE VALERIE LTD", company_number=None, directors=[])
    
adverse_media = media_agent.search_adverse_media()
print(adverse_media)
