from datetime import datetime

from langgraph.types import Command

import src.risklens2.graph.nodes as workflow_nodes
from src.risklens2.graph.workflow import workflow
from src.risklens2.models.company_research_schemas import (
    ChargesInfo,
    CompanyProfile,
    CompanyResearch,
    DirectorInfo,
    FilingsInfo,
    InsolvencyInfo,
)

def test_workflow_runs_to_completion(monkeypatch):
    company_research = CompanyResearch(
        company_profile=CompanyProfile(
            company_name="Test Ltd",
            company_number="12345678",
            status="Active",
            incorporation_date=datetime(2020, 1, 1),
            age=6,
            type="Private limited company",
            sic_code=[],
            industry_names=["Manufacturing"],
            reg_address={},
        ),
        director_details=DirectorInfo(
            directors=[{"name": "Jane Doe"}],
            secretary=[],
            others=[],
            director_count=1,
            total_officials=1,
            avg_director_tenure=3.0,
        ),
        psc_details={},
        filing_details=FilingsInfo(
            strike_off_action_flag=False,
            director_change_frequency_per_year=0,
        ),
        insolvency_details=InsolvencyInfo(),
        charges_details=ChargesInfo(secured_lenders=[]),
    )

    class FakeCompanyResearchAgent:
        def research(self, COMPANY_NUMBER):
            return company_research

    class FakeIndustryIntelligenceAgent:
        def __init__(self, industry_names):
            pass

        def analyse_industries(self):
            return {"result": "mock industry analysis"}

    class FakeMediaAgent:
        def __init__(self, **kwargs):
            pass

        def search_adverse_media(self):
            return {"result": "mock media analysis"}

    class FakeMemoAgent:
        def create_memo(self, **kwargs):
            return "Test credit memo"

    monkeypatch.setattr(workflow_nodes, "CompanyResearchAgent", FakeCompanyResearchAgent)
    monkeypatch.setattr(
        workflow_nodes, "IndustryIntelligenceAgent", FakeIndustryIntelligenceAgent
    )
    monkeypatch.setattr(workflow_nodes, "MediaAgent", FakeMediaAgent)
    monkeypatch.setattr(workflow_nodes, "MemoAgent", FakeMemoAgent)

    config = {"configurable": {"thread_id": "workflow-test-1"}}
    paused = workflow.invoke({"company_number": "12345678"}, config)

    assert "__interrupt__" in paused

    financials = {
        "revenue_cy": 15000000,
        "revenue_py": 10000000,
        "ebitda": 1200000,
        "net_profit": 650000,
        "cash": 450000,
        "current_assets": 3200000,
        "inventory": 750000,
        "current_liabilities": 2200000,
        "total_assets": 7800000,
        "total_liabilities": 4800000,
        "equity": 3000000,
        "total_debt": 2500000,
        "interest_expense": 180000,
    }
    result = workflow.invoke(Command(resume=financials), config)

    assert result["company_name"] == "Test Ltd"
    assert result["financial_analysis"].profitability.revenue_growth == 50.0
    assert result["policy_assessment"].recomendation == "APPROVE"
    assert result["credit_memo"] == "Test credit memo"