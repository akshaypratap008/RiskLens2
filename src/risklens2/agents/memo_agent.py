from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage
from pathlib import Path
from dotenv import load_dotenv
import yaml

from src.risklens2.models.financials_schemas import FinancialAnalysis, FinancialInput
from src.risklens2.models.policy_schemas import PolicyAssesment
from src.risklens2.models.company_research_schemas import CompanyResearch
from src.risklens2.utils import load_prompt

load_dotenv()

# load config
AGENT_CONFIG_FILE_PATH = Path(__file__).parents[0] / "agents_config.yaml"
with open(AGENT_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

LLM_MODEL = config['agents']['memo_agent']['llm_model']
LLM_TEMPRATURE = config['agents']['memo_agent']['llm_temprature']

class MemoAgent:
    """This Agent takes the company financials output from financial agent, policy output from policy agent, industry research output from industry inteligence agent, research output from company research agent, and output from adverse media agent and generates a credit memo."""

    def __init__(self):
        self.llm = ChatOpenAI(model = LLM_MODEL, temperature=LLM_TEMPRATURE)


    def create_memo(
            self,
            company_profile: FinancialInput,
            financial_analysis: FinancialAnalysis,
            policy_assesment: PolicyAssesment,
            industry_analysis: dict | None = None,
            media_analysis: dict | None = None, 
            company_research: CompanyResearch | None = None
    ):
        """Main function which uses LLM to generate the credit memo based on the company info and assesment results provided."""
        system_prompt, user_prompt = self._generate_prompt(
            company_profile,
            financial_analysis,
            policy_assesment,
            industry_analysis,
            media_analysis,
            company_research
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
            media_analysis: dict | None = None,
            company_research: CompanyResearch | None = None
    ):
        credit_memo_prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "credit_memo_prompt.yaml"
        
        prompt = load_prompt(credit_memo_prompt_path)
        system_prompt = prompt['system_prompt']
        user_prompt = f"{prompt['user_template'].format(
            company_profile = company_profile,
            financial_analysis = financial_analysis.model_dump_json(indent = 2),
            policy_assesment = policy_assesment.model_dump_json(indent = 2),
            industry_analysis = industry_analysis,
            media_analysis = media_analysis,
            company_research = company_research
        )}\n{prompt['output_format']}"

        return system_prompt, user_prompt