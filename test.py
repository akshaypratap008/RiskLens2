from src.risklens2.agents.financial_agent import FinancialAgent
from risklens2.models.financials_schemas import FinancialInput
from risklens2.agents.policy_agent import PolicyAgent
from risklens2.agents.memo_agent import MemoAgent
from risklens2.agents.company_research_agent import CompanyResearchAgent
from risklens2.agents.media_agent import MediaAgent
from risklens2.agents.industry_intelligence_agent import IndustryIntelligenceAgent
from src.risklens2.utils import load_prompt
from src.risklens2.graph.workflow import workflow

from langgraph.types import Command

import time
import json
from pathlib import Path

COMPANY_NUMBER = "SC196478"

# start = time.time()
# sample_company_data_path = Path("tests/sample_company.json")

# with open(sample_company_data_path, "rb") as file:
#     sample_test_json = json.load(file)

# company = sample_test_json['companies'][0]

# financials = FinancialInput.model_validate(company['financials'])
# print("INPUT FINANCIALS")
# print(financials)
# print("**************************************************\n")

# financial_agent = FinancialAgent()
# financial_analysis = financial_agent.analyse(financials)
# print("FINANCIAL ANALYSIS")
# print(financial_analysis)
# print("**************************************************\n")

# policy_agent = PolicyAgent()
# policy_assesment = policy_agent.evaluate(financial_analysis)
# print("POLICY ASSESMENT")
# print(policy_assesment)
# print("**************************************************\n")

# research_agent = CompanyResearchAgent()
# company_research = research_agent.research(COMPANY_NUMBER)
# print("COMPANY RESEARCH")
# print(company_research)
# print("**************************************************\n")

# industry_names = company_research.company_profile.industry_names
# industry_research_agent = IndustryIntelligenceAgent(industry_names=industry_names)
# industry_research = industry_research_agent.analyse_industries()
# print("INDUSTRY RESEARCH")
# print(industry_research)
# print("**************************************************\n")

# media_agent = MediaAgent(
#     company_number = COMPANY_NUMBER,
#     company_name = company_research.company_profile.company_name,
#     directors = [director["name"] for director in company_research.director_details.directors]
# )
# print("ADVERSE MEDIA")
# adverse_media = media_agent.search_adverse_media()
# print(adverse_media)
# print("**************************************************\n")

# memo_agent = MemoAgent()
# memo = memo_agent.create_memo(
#     company_profile=financials,
#     financial_analysis=financial_analysis,
#     policy_assesment=policy_assesment,
#     industry_analysis=industry_research,
#     media_analysis=adverse_media,
#     company_research=company_research
# )

# print("----MEMO---------------")
# print(memo)
# print("**************************************************\n")

# end = time.time()
# print("RUN TIME: ", end-start)

start = time.time()
initial_state = {
    "company_number": "SC196478"
}

config = {"configurable": {"thread_id": 1}}

workflow.invoke(initial_state, config)

final_state = workflow.invoke(
    Command(
        resume={
            "revenue_cy": 15000000,
            "revenue_py": 10000000,
            "ebitda": 1200000,
            "net_profit": 650000,
            "cash": 450000,
            "current_assets": 3200000,
            "inventory": 750000,
            "current_liabilities": 2200000,
            "total_assets": 7800000,
            "total_liabilities": 4800000,
            "equity": 3000000,
            "total_debt": 2500000,
            "interest_expense": 180000
        }
    ), config=config
)
end = time.time()

print(final_state)
print()
print("RUN TIME: ", end-start)




