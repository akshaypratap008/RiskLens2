from src.risklens2.credit_policy_rag.components.vector_store import VectorStore

from pathlib import Path
import yaml

RAG_CONFIG_FILE_PATH = Path(__file__).parents[1] / "rag_config.yaml"
with open(RAG_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

TOP_K = config['rag']['retriever']['top_k']

class Retriever:

    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(self, query: str):
        results = self.vector_store.query_search_with_score(query = query, top_k=TOP_K)
        return results
