from src.risklens2.agents.financial_agent import FinancialAgent
from src.risklens2.models.schemas import FinancialInput
import json
from pathlib import Path

sample_company_data_path = Path("tests/sample_company.json")

with open(sample_company_data_path, "rb") as file:
    sample_test_json = json.load(file)

agent = FinancialAgent()

for company in sample_test_json['companies']:
    financials = FinancialInput.model_validate(company['financials'])
    print(company['company_name'])
    results = agent.analyse(financials=financials)
    print(results)