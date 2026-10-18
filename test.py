from src.risklens2.agents.financial_agent import FinancialAgent
from risklens2.models.financials_schemas import FinancialInput
from risklens2.agents.policy_agent import PolicyAgent
import json
from pathlib import Path

sample_company_data_path = Path("tests/sample_company.json")

with open(sample_company_data_path, "rb") as file:
    sample_test_json = json.load(file)

financial_agent = FinancialAgent()
policy_agent = PolicyAgent()

for company in sample_test_json['companies']:
    financials = FinancialInput.model_validate(company['financials'])

    print(company['company_name'])
    analysis_results = financial_agent.analyse(financials=financials)
    print("-------FINANCIAL ANALYSIS AGENT RESULTS---------")
    print(analysis_results)
    print()

    policy_assesement = policy_agent.evaluate(analysis = analysis_results)
    print("-------POLICY AGENT RESULTS----------")
    print(policy_assesement)
    print(2*"*********************************************")
    