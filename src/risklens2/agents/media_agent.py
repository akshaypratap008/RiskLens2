from langchain_tavily import TavilySearch
from typesafe_sdk import TypeSafeClient, Noul

from src.risklens2.models.media_search_schemas import CompanyAdverseMedia

import yaml
from pathlib import Path
import os
from dotenv import load_dotenv

# load config
AGENT_CONFIG_FILE_PATH = Path(__file__).parents[0] / "agents_config.yaml"
with open(AGENT_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

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
    """This agent finds the adverse media information of the company. It uses the web search tool and JEV to clasify the news and return the adverse media info about the company and their directors. """

    def __init__(self, company_number: str, company_name: str, directors: list):
        self.company_number:str = company_number
        self.company_name:str = company_name
        self.directors:list = directors
    
        self.tavily_client = TavilySearch(
            max_results = MAX_RESULTS,
            topic = TOPIC,
            search_depth = SEARCH_DEPTH,
            exact_match = EXACT_MATCH
        )

        self.jev_client = TypeSafeClient(
            api_key=TYPESAFE_API_KEY,
            model = JEV_MODEL
        )

    def search_adverse_media(self):
        """
        The main function which uses tavily search to search the company using business name and directors names. The output from tavily search is fed to jev dicision model to classify if any critical falgs are present in the news articles. 
        """
        company_queries, drector_queries = self._generate_queries()

        adverse_media_flags = {}
        company_adverse_media_flags = []
        directors_adverse_media_flags = []

        # running company_quries search through tavily
        for query_flag, query in company_queries.items():
            search_output = self.tavily_client.invoke({"query": query})
            jev_result = self._evaluate_search_output(search_output=search_output, evaluation_type = "company_search_evaluation")
            for flag_type, result in jev_result.answers.items():
                if flag_type == query_flag:
                    threshold = 0.50
                else:
                    threshold = 0.75

                if result.noul >= threshold:
                    company_adverse_media_flags.append({
                        "flag_type": flag_type,
                        "jev_score": result.noul,
                        "url": search_output['results'][0]['url'],
                        "published_date": search_output['results'][0]['published_date'],
                        "tavily_search_confidence": search_output['results'][0]['score']
                    })

        for director_name, queries in drector_queries.items():
            for flag_type, query in queries.items():
                search_output = self.tavily_client.invoke({"query": query})
                jev_result = self._evaluate_search_output(search_output=search_output, evaluation_type = "director_search_evaluation", director_name = director_name)
                print(jev_result)
                for flag_type, result in jev_result.answers.items():
                    if flag_type == query_flag:
                        threshold = 0.50            # if the flag type being queried using jev is save as the main query flag
                    else:
                        threshold = 0.75            # if the flag type being queried using jev is different from the main query flag

                    if result.noul >= threshold:
                        directors_adverse_media_flags.append({
                            "director_name": director_name,
                            "flag_type": flag_type,
                            "jev_score": result.noul,
                            "url": search_output['results'][0]['url'],
                            "published_date": search_output['results'][0]['published_date'],
                            "tavily_search_confidence": search_output['results'][0]['score']
                        })

        adverse_media_flags['company_adverse_media_flags'] = company_adverse_media_flags
        adverse_media_flags['directors_adverse_media_flags'] = directors_adverse_media_flags
                
        return adverse_media_flags

        
    def _evaluate_search_output(self, search_output, evaluation_type, director_name= None):
        """
        This function takes the output from the tavily search and feeds it to jev to classify if any fraud, insolvency, legal, regulatory flags are present in the news aticles.
        Similarly for director search output, it uses jev to clasify if any fraud, disqualification or legal flags present. 
        It returns the jev output which includes the flag type, jev scores, director name where applicable.
        """

        if evaluation_type == "company_search_evaluation":
            # using jev, checking the core adverse_media metrics
            for item in search_output['results']:
                content = item['title'] + "\n" + item['content']        # concatinate the title and the actual content to feed to jev

                jev_response = self.jev_client.system_one(
                    state = content,
                    questions = {
                        "fraud_flag": Noul(
                            instructions = f"Based on this news article, does the company {self.company_name} seem to have been involved in fraud, corruption, bribery, money laundering or criminal investigation?"
                        ),

                        "insolvency_flag": Noul(
                            instructions = f"Based on this news article, does the company {self.company_name} indicate a risk of insolvency or has already gone into insolvency? Or is there any indication of liquidation or winding up orders?"
                        ),

                        "legal_flag": Noul(
                            instructions = f"Based on this news article, does the text indicate court litigation, criminal prosecution, lawsuits, or legal judgments against the conpamy {self.company_name}?"
                        ),

                        "regulatory_flag": Noul(
                            instructions = f"Based on this news article, does it indicate that the company {self.company_name} has had any regulatory enforcement, regulatory fines, official penalties or license revocation?"
                        )
                    }
                )

        elif evaluation_type == "director_search_evaluation":
            for item in search_output['results']:
                content = item['title'] + "\n" + item['content']        # concatinate the title and the actual content to feed to jev 

                jev_response = self.jev_client.system_one(
                    state = content,
                    questions = {
                        "fraud_flag" : Noul(
                            instructions = f"Based on this news article, does the person {director_name} seem to have been involved in fraud, corruption, bribery, money laundering or criminal investigation?"
                        ),
                        "disqualification_flag" : Noul(
                            instructions = f"Based on this news article, does the person {director_name} has been disqualified, barred, sanctioned or penalised for any wrong doings?"
                        ),
                        "legal_flag": Noul(
                            instructions= f"Based on this news article, has the person {director_name} ever been prosecuted, convicted by the courts or have a lawsuit against them?"
                        )
                    }
                )
        
        return jev_response

    
    def _generate_queries(self):
        """
        This function generates quesries for tavily search. 
        Returns: Company Specific Queries and Director specific queries
        """

        clean_name = self.company_name.replace(" LIMITED", "").replace(" LTD", "").strip()      # to search news articles including any alternate names of the company - does not include the trading name
        entity_names = f'("{self.company_name}" OR "{clean_name}")'

        company_queries = {
            "insolvency_flag": f'"{entity_names}" AND ("insolvency" OR "administration" OR "liquidation" OR "winding up" OR "creditors")',
            "fraud_flag": f'"{entity_names}" AND ("fraud" OR "bribery" OR "corruption" OR "money laundering" OR "investigation")',
            "legal_flag": f'"{entity_names}" AND ("litigation" OR "lawsuit" OR "prosecution" OR "court" OR "fine" OR "penalty")',
            "regulatory_flag": f'"{entity_names}" AND ("regulatory" OR "enforcement" OR "health and safety" OR "disqualification")'
        }

        director_queries = {}
        for director_name in self.directors:
            queries = {}        # will store fraud_query, disqualification query and legal query for each director

            director_context = f'{director_name} AND ("{self.company_name}" OR "{clean_name}" OR "director" OR "officer")'        # generates a context of similar meaning to feed to tavily

            queries["fraud_flag"] = f'{director_context} AND (fraud OR bribery OR corruption OR "money laundering" OR embezzlement OR "insider trading")'

            queries["disqualification_flag"] = f'{director_context} AND ("director disqualification" OR "disqualified" OR "barred" OR "sanction" OR "penalty" OR "enforcement" OR "fiduciary duty")'

            queries["legal_flag"] = f'{director_context} AND ("prosecution" OR "arrested" OR "indicted" OR "lawsuit" OR "court" OR "sentence" OR "conviction" OR "judgment")'

            director_queries[director_name] = queries

        return company_queries, director_queries
