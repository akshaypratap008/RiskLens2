from src.risklens2.credit_policy_rag.components.retriever import Retriever
from src.risklens2.credit_policy_rag.components.generator import ResponseGenerator

class RAGPipeline:
    """Full RAG pipeline"""

    def __init__(self, query:str):
        self.query = query
        self.retriever = Retriever()
        self.generator = ResponseGenerator()

    def run(self):
        retrieved_results = self.retriever.retrieve(
            query = self.query
        )

        reranked_results = self.retriever.rerank_docs(query = self.query, results = retrieved_results)

        response = self.generator.generate_response(
            query = self.query,
            retrieved_results= reranked_results
        )

        answer = response.answer
        sources = response.sources

        return answer, sources




