from pathlib import Path
import yaml
from dotenv import load_dotenv
import shutil
import sys

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from src.risklens2.logger import logging
from src.risklens2.exceptions import CustomException

load_dotenv()

RAG_CONFIG_FILE_PATH = Path(__file__).parents[1] / "rag_config.yaml"
with open(RAG_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

COLLECTION_NAME = config['rag']['vector_store']['chromadb']['collection_name']
VECTOR_STORE_PATH = config['rag']['vector_store']['chromadb']['persistant_dir']
EMBEDDING_MODEL_NAME = config['rag']['vector_store']['chromadb']['embedding_model']
COLLECTION_CONFIG = config['rag']['vector_store']['chromadb']['collection_configuration']           # collection_config is used to get the normalised similarity scores

class VectorStore:
    """Vector store to store embeddings"""

    def __init__(self):

        self.embeddings = OpenAIEmbeddings(
            model = EMBEDDING_MODEL_NAME
        )

        self.vector_store = Chroma(
            collection_name= COLLECTION_NAME,
            embedding_function= self.embeddings,
            persist_directory= VECTOR_STORE_PATH,
            collection_configuration=COLLECTION_CONFIG
        )

        logging.info("Vector Store initialised")

    def add_chunks(self, chunks:list):
        """Function to generate embeddings of the chunks and add them to the vector store"""

        try:
            texts = [chunk['content'] for chunk in chunks]
            metadatas = [chunk['metadata'] for chunk in chunks]
            ids = [chunk['metadata']['chunk_id'] for chunk in chunks]

            self.vector_store.add_texts(
                texts = texts,
                metadatas= metadatas,
                ids = ids
            )
            logging.info(f"{len(chunks)} chunks successfully added to vector store")
        except Exception as e:
            logging.exception(f"Failed to add {len(chunks)} chunks to the vector store")
            raise CustomException(e, sys)

    def query_search_with_score(self, query:str, top_k:int = 5) -> list[dict]:
        """Searches the vector store. Returns a list of dic with content, metadata and normalised similarity score for each chunk"""
        try:
            logging.info(f"Searching vector store for query: {query}")
            results = self.vector_store.similarity_search_with_relevance_scores(
                query=query,
                k = top_k
            )
            relevant_chunks = []

            for doc, score in results:
                relevant_chunks.append(
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "score": score
                    }
                )
            
            logging.info(f"Similarity search completed for the query: {query}")
            return relevant_chunks
        except Exception as e:
            logging.info(f"Failed to complete similarity search for query: {query}")
            raise CustomException(e, sys)
        

    def reset_vector_store(self):
        """Use this function to delete the vector store"""
        path = Path(VECTOR_STORE_PATH)

        if path.exists():
            shutil.rmtree(VECTOR_STORE_PATH)
        logging.info("vector store successfully deleted")




