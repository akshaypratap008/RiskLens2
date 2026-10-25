from typing import TypedDict
from src.risklens2.models.company_research_schemas import CompanyResearch
from src.risklens2.models.financials_schemas import FinancialInput, FinancialAnalysis
from src.risklens2.models.policy_schemas import PolicyAssessment
from src.risklens2.models.industry_intelligence_schemas import IndustryIntelligence
from src.risklens2.models.media_search_schemas import AdverseMediaInfo

class CreditState(TypedDict):
    company_number: str
    company_name: str | None
    company_research: CompanyResearch | None
    financials_inputs: FinancialInput | None
    financial_analysis: FinancialAnalysis | None
    policy_assessment: PolicyAssessment | None
    industry_analysis: IndustryIntelligence | None
    media_analysis: AdverseMediaInfo | None
    credit_memo: str | None