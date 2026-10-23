from langchain_tavily import TavilySearch

import yaml
from pathlib import Path
import os
from dotenv import load_dotenv

# load config
AGENT_CONFIG_FILE_PATH = Path(__file__).parents[0] / "agents_config.yaml"
with open(AGENT_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# tavily configs
MAX_RESULTS = config['agents']['industry_intelligence_agent']['tavily']['max_results']
TOPIC = config['agents']['industry_intelligence_agent']['tavily']['topic']
SEARCH_DEPTH = config['agents']['industry_intelligence_agent']['tavily']['search_depth']
INCLUDE_DOMAINS = config['agents']['industry_intelligence_agent']['tavily']['include_domains']
TAVILY_THRESHOLD = config['agents']['industry_intelligence_agent']['threshold']

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

    def analyse_industries(self):
        for industry in self.industry_names:
            queries = [
                f"UK {industry} industry outlook",
                f"UK {industry} key risks and challenges",
                f"UK {industry} insolvency trends",
                f"UK {industry} regulatory developments",
                f"UK {industry} impact of inflation and interest rates"
            ]

            for query in queries:
                search_results = self.tavily_client.invoke({"query": query})
                filtered_results = []          # those tavily search results which have score above the treshold will be added to it
                
                # filter results based on tavily confidence score
                for result in search_results:
                    if result['score'] >= TAVILY_THRESHOLD:
                        filtered_results.append(
                            {
                                "url": result['url'],
                                "title": result['title'],
                                "content": result['content']
                            }
                        )

                combined_context = "\n\n".join(
                    result['content'] for result in filtered_results
                )

                self._evaluate_research(combined_context)
                
                print(search_results)
                print()
                print("----------------------------------------------")

    def _evaluate_research(self, combined_context):
        pass