from src.risklens2.agents.financial_agent import FinancialAgent
from risklens2.models.financials_schemas import FinancialInput
from risklens2.agents.policy_agent import PolicyAgent
from risklens2.agents.memo_agent import MemoAgent
from risklens2.agents.company_research_agent import CompanyResearchAgent
from risklens2.agents.media_agent import MediaAgent
from risklens2.agents.industry_intelligence_agent import IndustryIntelligenceAgent
from src.risklens2.utils import load_prompt
from src.risklens2.graph.workflow import workflow
from src.risklens2.credit_policy_rag.components.chunker import CreditPolicyChunker
from src.risklens2.credit_policy_rag.components.vector_store import VectorStore
from src.risklens2.credit_policy_rag.components.retriever import Retriever
from src.risklens2.credit_policy_rag.evals.retirever_eval import RetrieverEval
from src.risklens2.credit_policy_rag.components.generator import ResponseGenerator
from src.risklens2.credit_policy_rag.rag_pipeline import RAGPipeline

from langgraph.types import Command

import time
import json
from pathlib import Path
import pickle

COMPANY_NUMBER = "SC196478"
CREDIT_POLICY_FILE_PATH = "data/credit_policy_extract_2.pdf"
# ----------------------------------------------------------------------------
# #AGENTS TESTING
# start = time.time()
# sample_company_data_path = Path("tests/sample_company.json")

# with open(sample_company_data_path, "rb") as file:
#     sample_test_json = json.load(file)

# company = sample_test_json['companies'][0]

# financials = FinancialInput.model_validate(company['financials'])
# print("INPUT FINANCIALS")
# print(financials)
# print("**************************************************\n")

# financial_agent = FinancialAgent()
# financial_analysis = financial_agent.analyse(financials)
# print("FINANCIAL ANALYSIS")
# print(financial_analysis)
# print("**************************************************\n")

# policy_agent = PolicyAgent()
# policy_assesment = policy_agent.evaluate(financial_analysis)
# print("POLICY ASSESMENT")
# print(policy_assesment)
# print("**************************************************\n")

# research_agent = CompanyResearchAgent()
# company_research = research_agent.research(COMPANY_NUMBER)
# print("COMPANY RESEARCH")
# print(company_research)
# print("**************************************************\n")

# industry_names = company_research.company_profile.industry_names
# industry_research_agent = IndustryIntelligenceAgent(industry_names=industry_names)
# industry_research = industry_research_agent.analyse_industries()
# print("INDUSTRY RESEARCH")
# print(industry_research)
# print("**************************************************\n")

# media_agent = MediaAgent(
#     company_number = COMPANY_NUMBER,
#     company_name = company_research.company_profile.company_name,
#     directors = [director["name"] for director in company_research.director_details.directors]
# )
# print("ADVERSE MEDIA")
# adverse_media = media_agent.search_adverse_media()
# print(adverse_media)
# print("**************************************************\n")

# memo_agent = MemoAgent()
# memo = memo_agent.create_memo(
#     company_profile=financials,
#     financial_analysis=financial_analysis,
#     policy_assesment=policy_assesment,
#     industry_analysis=industry_research,
#     media_analysis=adverse_media,
#     company_research=company_research
# )

# print("----MEMO---------------")
# print(memo)
# print("**************************************************\n")

# end = time.time()
# print("RUN TIME: ", end-start)

# ----------------------------------------------------------------------------------
# #WORKFLOW TESTING

# start = time.time()
# initial_state = {
#     "company_number": "SC196478"
# }

# config = {"configurable": {"thread_id": 1}}

# workflow.invoke(initial_state, config)

# final_state = workflow.invoke(
#     Command(
#         resume={
#             "revenue_cy": 15000000,
#             "revenue_py": 10000000,
#             "ebitda": 1200000,
#             "net_profit": 650000,
#             "cash": 450000,
#             "current_assets": 3200000,
#             "inventory": 750000,
#             "current_liabilities": 2200000,
#             "total_assets": 7800000,
#             "total_liabilities": 4800000,
#             "equity": 3000000,
#             "total_debt": 2500000,
#             "interest_expense": 180000
#         }
#     ), config=config
# )
# end = time.time()

# print(final_state)
# print()
# print("RUN TIME: ", end-start)

# -----------------------------------------------------------------------
# #CHUNKER TESTING
# chunker = CreditPolicyChunker()

# docling_doc = chunker.convert_to_doc(CREDIT_POLICY_FILE_PATH)
# print(docling_doc)

# with open("data/artifacts/docling_chunks.pkl", "rb") as file:
#     docling_chunks = pickle.load(file)

# doc_doc = chunker.convert_to_doc(CREDIT_POLICY_FILE_PATH)

# chunks = chunker.create_chunks(doc = doc_doc)

# for chunk in chunks:
#     print(type(chunk))
#     print()

# print(len(chunks))

# with open("data/artifacts/credit_policy_chunks.pkl", "wb") as f:
#     pickle.dump(chunks, f)

# #RETRIEVER TESTING - using vectorstore class
with open("data/artifacts/credit_policy_chunks.pkl", "rb") as file:
    chunks = pickle.load(file)

# vector_store= VectorStore()

# query = "What is the minimum DSCR for hospitality lending?"
# results = vector_store.query_search_with_score(query=query)
# print(results)

# #RETRIEVER TESTING - using retriever class
# query = "What is the minimum DSCR for hospitality lending?"

# start = time.time()
# with open("data/artifacts/credit_policy_chunks.pkl", "rb") as file:
#     chunks = pickle.load(file)

# vector_store= VectorStore()
# vector_store.add_chunks(chunks)
# print("vector store build")

# retriever = Retriever()
# result = retriever.retrieve(query=query)
# end = time.time()

# print("------------RESULTS---------------")
# print(result)
# print()
# print("run time:", end-start)

# #RETRIEVAL EVALS test
start = time.time()
evaluator = RetrieverEval(eval_description="reranker retriever")

evaluator.run_evals()
end = time.time()

print("run time:", end-start)

# #GENERATOR TEST
# start = time.time()
# query = "The applicant is a UK limited company that has been trading for 18 months. Can it be assessed under the standard SME credit policy?"

# rag = ResponseGenerator()
# retriver = Retriever()

# retrieved_docs = retriver.retrieve(query = query)

# response = rag.generate_response(
#     query= query,
#     retrieved_results=retrieved_docs
# )

# end = time.time()
# print(response)
# print()
# print("run time:", end-start)

# #RAG PIPELINE TEST
# start = time.time()
# query = "What are the DSCR thresholds in the policy — what's considered strong, what's the minimum, and when is it an outright decline?"
# rag_pipeline = RAGPipeline(query=query)
# rag_pipeline.run()
# # answer, sources = rag_pipeline.run()
# # print("ANSWER: ", answer)
# # print("-----------")
# # print("SOURCES: ", sources)

# end = time.time()
# print()
# print("RUN TIME: ", end-start)



'''
ANSWER:  The policy treats the hospitality sector, including restaurants, as having specific risks and key metrics for assconsumption, labor costs, and fluctuations in consumer demand, along with high failure rates in the sector. The key ratiosin, the fixed charge coverage ratio (FCCRC), and revenue per available room (RevPAR). Stress scenarios for hospitality invcosts by 50%, and wage increases of 8%. Excessive leverage is mitigated with a maximum senior leverage of 2.5x and a debt dditionally, to be eligible for lending, the entity must have a trading history of at least 3 years and show resilience toty to manage operational risks.
-----------
SOURCES:  [Source(pages=[19, 20], section='30. Sector-Specific Underwriting', source_doc='credit_policy_extract_2.pdf', churce(pages=[16], section='14.4 Sector-specific stresses', source_doc='credit_policy_extract_2.pdf', chunk_id='79f62457-1ee
'''