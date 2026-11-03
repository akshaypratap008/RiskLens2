from pathlib import Path
import yaml
import json
from dotenv import load_dotenv

from deepeval.test_case import LLMTestCase
from deepeval.metrics import (ContextualPrecisionMetric, ContextualRecallMetric)
from deepeval import evaluate
from deepeval.evaluate import DisplayConfig

from src.risklens2.credit_policy_rag.components.retriever import Retriever

load_dotenv()

RAG_CONFIG_FILE_PATH = Path(__file__).parents[1] / "rag_config.yaml"
with open(RAG_CONFIG_FILE_PATH, "r") as f:
    config = yaml.safe_load(f)

GOLDENS_FOLDER_PATH = config["rag"]["evals"]["goldens_folder_path"]
DATSET_NAME = config["rag"]["evals"]['retriever_eval']['dataset_name']
EVAL_METRICS_PARAMETERS = config["rag"]["evals"]['retriever_eval']['eval_metrics_parameters']
EVAL_RESULTS_FOLDER = config["rag"]["evals"]["eval_results_folder_path"]

class RetrieverEval:
    """Evaluates the retrieval results using deepeval"""

    def __init__(self, eval_description: str):
        self.retriever = Retriever()
        self.eval_description = eval_description

    def _build_test_cases(self) -> list[LLMTestCase]:
        goldens_doc = self._load_goldens_json()
        test_cases = []
        for item in goldens_doc:
            input = item['input']
            expected_output = item['expected_output']

            actual_retrieval_output = self.retriever.retrieve(
                query = item['input']
            )

            retrieval_context = [result['content'] for result in actual_retrieval_output]
            test_cases.append(LLMTestCase(
                input = input,
                actual_output= "generator not evaluated in this run",
                expected_output=expected_output,
                retrieval_context=retrieval_context
            ))
        return test_cases

    def _load_goldens_json(dataset:str = DATSET_NAME):
        """loads the golden dataset and returns a python object which can be iterated"""
        file_path = Path(GOLDENS_FOLDER_PATH) / DATSET_NAME
        with open(file_path, 'rb') as file:
            goldens = json.load(file)
        return goldens

    def run_evals(self):
        test_cases = self._build_test_cases()
        metrics = [
            ContextualRecallMetric(**EVAL_METRICS_PARAMETERS),
            ContextualPrecisionMetric(**EVAL_METRICS_PARAMETERS)
        ]

        result = evaluate(
            test_cases=test_cases,
            metrics=metrics,
            hyperparameters={
                "retriever": self.eval_description,
                "chunker": config['rag']['chunker']['strategy'],
                "embedding_model": config['rag']['vector_store']['chromadb']['embedding_model'],
                "top_k": config['rag']['retriever']['top_k'],
                "judge_model": config['rag']['evals']['retriever_eval']['eval_metrics_parameters']['model'],
                "golden_dataset_name": config['rag']['evals']['retriever_eval']['dataset_name']
            },
            display_config=DisplayConfig(results_folder=EVAL_RESULTS_FOLDER)
        )

        return result



    