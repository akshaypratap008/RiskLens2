from src.risklens2.credit_policy_rag.components.vector_store import VectorStore
from src.risklens2.logger import logging
from src.risklens2.exceptions import CustomException

from pathlib import Path
import yaml
import sys

from sentence_transformers import CrossEncoder

RAG_CONFIG_FILE_PATH = Path(__file__).parents[1] / "rag_config.yaml"
with open(RAG_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

RETRIEVR_TOP_K = config['rag']['retriever']['top_k']
RERANKER_MODEL = config['rag']['reranker']['model']
RERANKER_TOP_K = config['rag']['reranker']['top_k']



class Retriever:

    def __init__(self):
        self.vector_store = VectorStore()
        self.reranker = CrossEncoder(RERANKER_MODEL)

    def retrieve(self, query: str):
        """Retrieve top_k results for the query"""
        try:
            logging.info(f"Retrieval started for query: {query}")
            results = self.vector_store.query_search_with_score(query = query, top_k=RETRIEVR_TOP_K)

            logging.info(f"Retrieval completed for query: {query}")
            return results
        except Exception as e:
            logging.exception(f"Retrieval failed for query: {query}")
            raise CustomException(e, sys)
        
    def rerank_docs(self, query:str, results:list[dict]) -> list[dict]:
        """Rerank retrieved docs using Cross encoder reranker. Add reranker scores to the existing dict for each doc, sort them and pick top_k results"""
        pairs = [(query, result['content']) for result in results]
        reranked_scores = self.reranker.predict(pairs)

        for result, reranked_scores in zip(results, reranked_scores):
            result["reranked_scores"] = float(reranked_scores)

        reranked_results = sorted(
            results,
            key = lambda x: x['reranked_scores'],
            reverse = True
        )

        top_results = reranked_results[:RERANKER_TOP_K]

        return top_results
