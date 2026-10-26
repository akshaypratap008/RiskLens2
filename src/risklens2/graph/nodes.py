from src.risklens2.graph.state import CreditState
from src.risklens2.agents.company_research_agent import CompanyResearchAgent
from src.risklens2.agents.industry_intelligence_agent import IndustryIntelligenceAgent
from src.risklens2.agents.media_agent import MediaAgent
from src.risklens2.agents.financial_agent import FinancialInput, FinancialAgent
from src.risklens2.agents.policy_agent import PolicyAgent
from src.risklens2.agents.memo_agent import MemoAgent
from src.risklens2.logger import logging
from src.risklens2.exceptions import CustomException

from langgraph.types import interrupt
from pydantic import ValidationError

import sys

def company_research(state: CreditState) -> dict:
    company_number = state['company_number']
    logging.info(f"Starting Company Research for company_number: {company_number}")

    company_research_agent = CompanyResearchAgent()

    try:
        company_info = company_research_agent.research(COMPANY_NUMBER=company_number)
        
        logging.info(f"Company research COMPLETED for company_number: {company_number}")

        return {
            "company_number": company_number,
            "company_name": company_info.company_profile.company_name,
            "company_research": company_info
        }
    except Exception as e:
        logging.exception(f"Company Research FAILED for company_number: {company_number}")
        raise CustomException(e, sys) from e


def industry_research(state: CreditState) -> dict:
    industry_names = state['company_research'].company_profile.industry_names
    industry_research_agent = IndustryIntelligenceAgent(industry_names = industry_names)

    logging.info(f"Industry Research STARTED for industry_names: {industry_names}")

    try:
        industry_analysis = industry_research_agent.analyse_industries()

        logging.info(f"Industry Research COMPLETED for industry_names: {industry_names}")
        return {
            "industry_analysis": industry_analysis
        }
    except Exception as e:
        logging.exception(f"Industry Research FAILED for industry_names: {industry_names}")
        raise CustomException(e, sys) from e
   

def media_research(state: CreditState) -> dict:
    logging.info(f"Adverse Media research STARTED for {state['company_name']}")

    try:
        media_research_agent = MediaAgent(
            company_name=state['company_name'],
            company_number=state['company_name'],
            directors= [director['name'] for director in state['company_research'].director_details.directors]
        )
        media_analysis = media_research_agent.search_adverse_media()

        logging.info(f"Adverse Media research COMPLETED for {state['company_name']}")
        return {
            "media_analysis" : media_analysis
        }
    except Exception as e:
        logging.exception(f"Adverse Media research FAILED for {state['company_name']}")
        raise CustomException(e, sys) from e

def get_financials_input(state: CreditState) -> dict:
    logging.info("Requesting financial inputs")

    financials_data = interrupt({
        "type": "financials_input"
    })

    try:
        financials = FinancialInput(**financials_data)
    except ValidationError:
        logging.exception(f"Financial Input validation failed for {state['company_name']}")
        raise

    logging.info(f"Financial Inputs received and validated for {state['company_name']}")
    return {
        "financials_inputs": financials
    }
    

def financial_analysis(state: CreditState) -> dict:
    logging.info(f"Financial Ratios calculations STARTED for {state['company_name']}")

    try:
        financial_agent = FinancialAgent()
        financial_analysis = financial_agent.analyse(financials= state['financials_inputs'])

        logging.info(f"Financial Ratios calculated for {state['company_name']}")
        return {
            "financial_analysis" : financial_analysis
        }
    
    except Exception as e:
        logging.exception(f"Financial Ratio calculation failed for {state['company_name']}")
        raise CustomException(e, sys) from e


def policy_assessment(state: CreditState) -> dict:
    logging.info(f"Policy Assessment started for {state['company_name']}")

    try:
        policy_agent = PolicyAgent()
        policy_assessment = policy_agent.evaluate(analysis=state['financial_analysis'])

        logging.info(f"Policy assessment completed for {state['company_name']}")
        return {
            "policy_assessment": policy_assessment
        }
    except Exception as e:
        logging.exception(f"Policy Assessment process failed for {state['company_name']}")
        raise CustomException(e, sys) from e


def credit_memo(state: CreditState) -> dict:
    logging.info(f"Credit memo generation started for {state['company_name']}")

    try:
        credit_memo_agent = MemoAgent()
        credit_memo = credit_memo_agent.create_memo(
            company_profile = state['financials_inputs'],
            financial_analysis= state['financial_analysis'],
            policy_assesment= state['policy_assessment'],
            industry_analysis= state['industry_analysis'],
            media_analysis= state['media_analysis'],
            company_research=state['company_research']
        )

        logging.info(f"Credit memo successfully generated for {state['company_name']}")
        return {
            "credit_memo": credit_memo
        }
    except Exception as e:
        logging.exception(f"Credit Memo generation failed")
        raise CustomException(e, sys) from e
