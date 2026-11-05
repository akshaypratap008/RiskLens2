from src.risklens2.utils import load_prompt
from src.risklens2.models.credit_policy_rag_schema import RAGResponse

from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage

from pathlib import Path
import yaml
from dotenv import load_dotenv

RAG_CONFIG_FILE_PATH = Path(__file__).parents[1] / "rag_config.yaml"
with open(RAG_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

load_dotenv()

LLM_MODEL = config['rag']['generator']['model']

class ResponseGenerator:

    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL
        ).with_structured_output(RAGResponse)

    def generate_response(self, query:str, retrieved_results: list[dict]) -> RAGResponse:
        system_prompt, user_prompt = self._build_final_prompt(
            query = query,
            retrieved_results=retrieved_results
        )

        response = self.llm.invoke([
            SystemMessage(content = system_prompt),
            HumanMessage(content = user_prompt)
        ])

        return response      

    def _generate_context_from_retrieved_docs(self, retrieved_results: list[dict]):
        retrieved_context = ""        
        for doc in retrieved_results:
            retrieved_context += f"""
Source Doc: {doc['metadata'].get("document_name", "Unknown")}
Section: {doc['metadata'].get("section", "Unknown")}
Pages: {doc['metadata'].get("pages", "Unknown")}
Chunk_id: {doc['metadata']['chunk_id']}

{doc['content']}
"""
        return "\n".join(retrieved_context)

    def _build_final_prompt(self, query:str, retrieved_results: list[dict]):
        credit_policy_rag_pompt_path = Path(__file__).resolve().parents[2] / "prompts" / "credit_policy_rag_prompt.yaml"
        
        prompt = load_prompt(
            file_path=credit_policy_rag_pompt_path
        )

        system_prompt = f"{prompt['system_prompt']}\n{prompt['output_guidelines']}"
        user_prompt = f"{prompt['user_template'].format(
            query = query,
            context = self._generate_context_from_retrieved_docs(
                retrieved_results= retrieved_results
            )
        )}"

        return system_prompt, user_prompt
