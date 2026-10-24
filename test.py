from src.risklens2.agents.financial_agent import FinancialAgent
from risklens2.models.financials_schemas import FinancialInput
from risklens2.agents.policy_agent import PolicyAgent
from risklens2.agents.memo_agent import MemoAgent
from risklens2.agents.company_research_agent import CompanyResearchAgent
from risklens2.agents.media_agent import MediaAgent
from risklens2.agents.industry_intelligence_agent import IndustryIntelligenceAgent
from src.risklens2.utils import load_prompt
import time

import json
from pathlib import Path

COMPANY_NUMBER = "15859635"

start = time.time()
sample_company_data_path = Path("tests/sample_company.json")

with open(sample_company_data_path, "rb") as file:
    sample_test_json = json.load(file)

company = sample_test_json['companies'][0]

financials = FinancialInput.model_validate(company['financials'])
print("INPUT FINANCIALS")
print(financials)
print("**************************************************\n")

financial_agent = FinancialAgent()
financial_analysis = financial_agent.analyse(financials)
print("FINANCIAL ANALYSIS")
print(financial_analysis)
print("**************************************************\n")

policy_agent = PolicyAgent()
policy_assesment = policy_agent.evaluate(financial_analysis)
print("POLICY ASSESMENT")
print(policy_assesment)
print("**************************************************\n")

research_agent = CompanyResearchAgent()
company_research = research_agent.research(COMPANY_NUMBER)
print("COMPANY RESEARCH")
print(company_research)
print("**************************************************\n")

industry_names = company_research.company_profile.industry_names
industry_research_agent = IndustryIntelligenceAgent(industry_names=industry_names)
industry_research = industry_research_agent.analyse_industries()
print("INDUSTRY RESEARCH")
print(industry_research)
print("**************************************************\n")

media_agent = MediaAgent(
    company_number = COMPANY_NUMBER,
    company_name = company_research.company_profile.company_name,
    directors = [director["name"] for director in company_research.director_details.directors]
)
print("ADVERSE MEDIA")
adverse_media = media_agent.search_adverse_media()
print(adverse_media)
print("**************************************************\n")

memo_agent = MemoAgent()
memo = memo_agent.create_memo(
    company_profile=financials,
    financial_analysis=financial_analysis,
    policy_assesment=policy_assesment,
    industry_analysis=industry_research,
    media_analysis=adverse_media,
    company_research=company_research
)

print("----MEMO---------------")
print(memo)
print("**************************************************\n")

end = time.time()
print("RUNT TIME: ", end-start)












print("RUN TIME: ", end-start)






