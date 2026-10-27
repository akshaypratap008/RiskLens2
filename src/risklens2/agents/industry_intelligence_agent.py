from langchain_tavily import TavilySearch

import yaml
from pathlib import Path
import os
from dotenv import load_dotenv
from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage

from src.risklens2.utils import load_prompt
from src.risklens2.models.industry_intelligence_schemas import IndustryIntelligence, IndustryOutlook, KeyIndustryRisks, InsolvencyTrend, RegulatoryRisks, MacroeconomicSentivity

# load config
AGENT_CONFIG_FILE_PATH = Path(__file__).parents[0] / "agents_config.yaml"
with open(AGENT_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

# tavily configs
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MAX_RESULTS = config['agents']['industry_intelligence_agent']['tavily']['max_results']
TOPIC = config['agents']['industry_intelligence_agent']['tavily']['topic']
SEARCH_DEPTH = config['agents']['industry_intelligence_agent']['tavily']['search_depth']
INCLUDE_DOMAINS = config['agents']['industry_intelligence_agent']['tavily']['include_domains']
TAVILY_THRESHOLD = config['agents']['industry_intelligence_agent']['tavily']['threshold']

# llm configs
LLM_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = config['agents']['industry_intelligence_agent']['llm']['model']
LLM_TEMPRATURE = config['agents']['industry_intelligence_agent']['llm']['temprature']

load_dotenv()

class IndustryIntelligenceAgent:
    """This agent performs industry research by using tavily to search external websites for industry outlook, risk factors, macroeconomic senstivity, regulatory risks and insolvency risks."""

    def __init__(self, industry_names:list):
        self.industry_names = industry_names
        self.tavily_client = TavilySearch(
            max_results = MAX_RESULTS,
            topic = TOPIC,
            search_depth = SEARCH_DEPTH,
            include_domains = INCLUDE_DOMAINS
        )
        self.llm = ChatOpenAI(model = LLM_MODEL, temperature=LLM_TEMPRATURE)

    def analyse_industries(self):
        if not self.industry_names:
            raise ValueError("No industry name supplied")

        primary_industry = self.industry_names[0]

        queries = {
            "industry_outlook": f"UK {primary_industry} industry outlook",
            "key_industry_risks": f"UK {primary_industry} key risks and challenges",
            "insolvency_trends": f"UK {primary_industry} insolvency trends",
            "regulatory_risks": f"UK {primary_industry} regulatory developments",
            "macroeconomic_senstivity": f"UK {primary_industry} impact of inflation and interest rates"
        }

        results: Dict[str, Any] = {}

        for query_type, query in queries.items():
            print(f"{query_type} being queried and evaluated")
            search_output = self.tavily_client.invoke({"query": query})
            filtered_results = []          # those tavily search results which have score above the treshold will be added to it
            
            # filter results based on tavily confidence score
            for result in search_output.get("results", {}):
                if result['score'] >= TAVILY_THRESHOLD:
                    filtered_results.append(
                        {
                            "url": result['url'],
                            "title": result['title'],
                            "content": result['content']
                        }
                    )
    
            combined_context = self._combine_context(filtered_results=filtered_results)
            response = self._evaluate_research(query_type = query_type, industry_name=primary_industry, combined_context = combined_context)

            results[query_type] = response

        return IndustryIntelligence(
            industry_name = primary_industry,
            industry_outlook=results["industry_outlook"],
            key_industry_risks = results['key_industry_risks'],
            insolvency_trends = results['insolvency_trends'],
            regulatory_risks = results['regulatory_risks'],
            macroeconomic_senstivity = results['macroeconomic_senstivity']
        )


    def _combine_context(self, filtered_results: list[dict]):
        combined_context = ''
        for i, result in enumerate(filtered_results):
            combined_context += f"""
Source {i}
Title: {result['title']}

URL: {result['url']}

Content: {result['content']}
----------------------------------

"""
            return combined_context

    def _evaluate_research(self, query_type: str, industry_name:str, combined_context: str):
        industry_intelligence_file_path = Path(__file__).resolve().parents[1] / "prompts" / "industry_intelligence_prompt.yaml"

        prompt = load_prompt(industry_intelligence_file_path)

        # get the right prompt and output schema based on the query type
        prompt_type = f"{query_type}_prompt"
        output_schema_map = {
            "industry_outlook": IndustryOutlook,
            "key_industry_risks": KeyIndustryRisks,
            "insolvency_trends": InsolvencyTrend,
            "regulatory_risks": RegulatoryRisks,
            "macroeconomic_senstivity": MacroeconomicSentivity
        }

        # system prompt depends on the type of query being evaluated by the llm
        # output format also depends on the type of query being evaluated
        system_prompt = prompt['system_prompts'][prompt_type]
        user_prompt = f"{prompt['user_template'].format(
            industry_name = industry_name,
            search_content = combined_context
        )}\nOutput format:\n{prompt['output_format'][query_type]}"

        outlook_llm = self.llm.with_structured_output(output_schema_map[query_type])
        response = outlook_llm.invoke([
            SystemMessage(content = system_prompt),
            HumanMessage(content = user_prompt)
        ])

        return response

    