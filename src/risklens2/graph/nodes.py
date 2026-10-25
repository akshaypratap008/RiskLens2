from src.risklens2.graph.state import CreditState
from src.risklens2.agents.company_research_agent import CompanyResearchAgent
from src.risklens2.agents.industry_intelligence_agent import IndustryIntelligenceAgent
from src.risklens2.agents.media_agent import MediaAgent
from src.risklens2.agents.financial_agent import FinancialInput, FinancialAgent
from src.risklens2.agents.policy_agent import PolicyAgent
from src.risklens2.agents.memo_agent import MemoAgent

from langgraph.types import interrupt

def company_research(state: CreditState) -> dict:
    company_number = state['company_number']

    company_research_agent = CompanyResearchAgent()
    company_info = company_research_agent.research(COMPANY_NUMBER=company_number)

    return {
        "company_number": company_number,
        "company_name": company_info.company_profile.company_name,
        "company_research": company_info
    }

def industry_research(state: CreditState) -> dict:
    industry_names = state['company_research'].company_profile.industry_names
    industry_research_agent = IndustryIntelligenceAgent(industry_names = industry_names)
    industry_analysis = industry_research_agent.analyse_industries()

    return {
        "industry_analysis": industry_analysis
    }

def media_research(state: CreditState) -> dict:
    media_research_agent = MediaAgent(
        company_name=state['company_name'],
        company_number=state['company_name'],
        directors= [director['name'] for director in state['company_research'].director_details.directors]
    )
    media_analysis = media_research_agent.search_adverse_media()

    return {
        "media_analysis" : media_analysis
    }

def get_financials_input(state: CreditState) -> dict:
    financials_data = interrupt({
        "type": "financials_input"
    })

    return {
        "financials_inputs": FinancialInput(**financials_data)
    }

def financial_analysis(state: CreditState) -> dict:
    financial_agent = FinancialAgent()
    financial_analysis = financial_agent.analyse(financials= state['financials_inputs'])
    return {
        "financial_analysis" : financial_analysis
    }


def policy_assessment(state: CreditState) -> dict:
    policy_agent = PolicyAgent()
    policy_assessment = policy_agent.evaluate(analysis=state['financial_analysis'])

    return {
        "policy_assessment": policy_assessment
    }


def credit_memo(state: CreditState) -> dict:
    credit_memo_agent = MemoAgent()
    credit_memo = credit_memo_agent.create_memo(
        company_profile = state['financials_inputs'],
        financial_analysis= state['financial_analysis'],
        policy_assesment= state['policy_assessment'],
        industry_analysis= state['industry_analysis'],
        media_analysis= state['media_analysis'],
        company_research=state['company_research']
    )

    return {
        "credit_memo": credit_memo
    }
