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

        # check if reranking is required - if the difference between normalised similarity scores of the first 2 docs is very low.
        # if the spread of max and min score is very high in the first 5 chunks, no reranking needed
        scores = [result['score'] for result in retrieved_results[:5]]
        print("Similarity scores of retrieved docs without reranker: ", scores)

        spread = max(scores) - min(scores)
        print("Spread of max-min scores: ", spread)

        top_5_retrieved = [result['score'] for result in retrieved_results[:5]]
        print("original: ", top_5_retrieved)

        # -----------------------
        reranked_results = self.retriever.rerank_docs(query = self.query, results = retrieved_results)

        top_5_reranked = [result['score'] for result in reranked_results]
        print("reranked: ", top_5_reranked)

        # response = self.generator.generate_response(
        #     query = self.query,
        #     retrieved_results= reranked_results
        # )

        # answer = response.answer
        # sources = response.sources

        # return answer, sources




