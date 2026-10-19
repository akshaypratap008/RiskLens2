from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage
from pathlib import Path
from dotenv import load_dotenv

from src.risklens2.models.financials_schemas import FinancialAnalysis, FinancialInput
from src.risklens2.models.policy_schemas import PolicyAssesment
from src.risklens2.utils import load_prompt

load_dotenv()

LLM_MODEL = "gpt-5"

class MemoAgent:
    """This Agent takes the company financials output from financial agent, policy output from policy agent, industry research output from industry inteligence agent, research output from company research agent, and output from adverse media agent and generates a credit memo."""

    def __init__(self):
        self.llm = ChatOpenAI(model = LLM_MODEL, temperature=0)


    def create_memo(
            self,
            company_profile: FinancialInput,
            financial_analysis: FinancialAnalysis,
            policy_assesment: PolicyAssesment,
            industry_analysis: dict | None = None,
            media_analysis: dict | None = None
    ):
        """Main function which uses LLM to generate the credit memo based on the company info and assesment results provided."""
        system_prompt, user_prompt = self._generate_prompt(
            company_profile,
            financial_analysis,
            policy_assesment,
            industry_analysis,
            media_analysis
        )

        response = self.llm.invoke([
            SystemMessage(content = system_prompt),
            HumanMessage(content = user_prompt)
        ])

        return response.content

    def _generate_prompt(
            self,
            company_profile: dict,
            financial_analysis: FinancialAnalysis,
            policy_assesment: PolicyAssesment,
            industry_analysis: dict | None = None,
            media_analysis: dict | None = None
    ):
        credit_memo_prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "credit_memo_prompt.yaml"
        prompt = load_prompt(credit_memo_prompt_path)
        system_prompt = prompt['system_prompt']
        user_prompt = f"{prompt['user_template'].format(
            company_profile = company_profile,
            financial_analysis = financial_analysis.model_dump_json(indent = 2),
            policy_assesment = policy_assesment.model_dump_json(indent = 2),
            industry_analysis = industry_analysis,
            media_analysis = media_analysis
        )}\n{prompt['output_format']}"

        return system_prompt, user_prompt