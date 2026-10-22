from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from typesafe_sdk import TypeSafeClient, Noul

import yaml
from pathlib import Path
import os
from dotenv import load_dotenv

# load config
AGENT_CONFIG_FILE_PATH = Path(__file__).parents[0] / "agents_config.yaml"
with open(AGENT_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

# llm configs
LLM_MODEL = config['agents']['media_agent']['llm_model']
LLM_TEMPRATURE = config['agents']['media_agent']['llm_temprature']

# tavily configs
MAX_RESULTS = config['agents']['media_agent']['tavily']['max_results']
TOPIC = config['agents']['media_agent']['tavily']['topic']
SEARCH_DEPTH = config['agents']['media_agent']['tavily']['search_depth']
EXACT_MATCH = config['agents']['media_agent']['tavily']['exact_match']

# jev configs
JEV_MODEL = config['agents']['media_agent']['jev_model']

# api keys
LLM_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TYPESAFE_API_KEY = os.getenv("TYPESAFE_API_KEY")


load_dotenv()

class MediaAgent:
    """This agent finds the adverse media information of the company. It uses the web search tools. Classifies the risk, give it a severity score."""

    def __init__(self, company_number: str, company_name: str, directors: list):
        self.company_number:str = company_number
        self.company_name:str = company_name
        self.directors:list = directors
        llm = ChatOpenAI(model = LLM_MODEL, temperature= LLM_TEMPRATURE)

    def search_adverse_media(self):
        company_queries, drector_queries = self._generate_queries()

        fraud_risk = {}

        # running company_quries search through tavily
        for query in company_queries:
            tavily_search = TavilySearch(
                max_results = MAX_RESULTS,
                topic = TOPIC,
                search_depth = SEARCH_DEPTH,
                exact_match = EXACT_MATCH
            )

            output = tavily_search.invoke({"query": query})

            # using jev, checking the core adverse_media metrics
            for item in output['results']:
                content = item['title'] + "\n" + item['content']        # concatinate the title and the actual content to feed to jev

                client = TypeSafeClient(
                    api_key=TYPESAFE_API_KEY,
                    model = JEV_MODEL
                )

                response = client.system_one(
                    state = content,
                    questions = {
                        "fraud_flags": Noul(
                            instructions = f"Based on this news article, does the company {self.company_name} seem to have been involved in fraud, corruption, bribery, money laundering or criminal investigation?"
                        ),

                        "insolvency_flags": Noul(
                            instructions = "Based on this news article, does the company indicate a risk of insolvency or has already gone into insolvency? Or is there any indication of liquidation or winding up orders?"
                        ),

                        "legal_flags": Noul(
                            instructions = "Based on this news article, does the text indicate court litigation, criminal prosecution, lawsuits, or legal judgments?"
                        ),

                        "regulatory_flag": Noul(
                            instructions = "Based on this news article, "
                        )
                    }
                )



    def _generate_queries(self):
        clean_name = self.company_name.replace(" LIMITED", "").replace(" LTD", "").strip()      # to search news articles including any alternate names of the company - does not include the trading name
        entity_names = f'("{self.company_name}" OR "{clean_name}")'


        company_queries = [
            f'"{entity_names}" AND ("insolvency" OR "administration" OR "liquidation" OR "winding up" OR "creditors")',
            f'"{entity_names}" AND ("fraud" OR "bribery" OR "corruption" OR "money laundering" OR "investigation")',
            f'"{entity_names}" AND ("litigation" OR "lawsuit" OR "prosecution" OR "court" OR "fine" OR "penalty")',
            f'"{entity_names}" AND ("regulatory" OR "enforcement" OR "health and safety" OR "disqualification")'
        ]

        director_queries = []
        for director_name in self.directors:
            director_context = f'"{director_name}" AND ("{self.company_name}" OR "{clean_name}" OR "director" OR "officer")'

            director_queries.append(f'{director_context} AND (fraud OR bribery OR corruption OR "money laundering" OR embezzlement OR "insider trading")')

            director_queries.append(f'{director_context} AND ("director disqualification" OR "disqualified" OR "barred" OR "sanction" OR "penalty" OR "enforcement" OR "fiduciary duty")')

            director_queries.append(f'{director_context} AND ("prosecution" OR "arrested" OR "indicted" OR "lawsuit" OR "court" OR "sentence" OR "conviction" OR "judgment")')

        return company_queries, director_queries
