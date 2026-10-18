agentic-credit-intelligence/
│
├── README.md
├── requirements.txt
├── .env
│
├── app/
│   │
│   ├── main.py
│   ├── api.py
│   │
│   ├── graph/
│   │   ├── workflow.py
│   │   ├── state.py
│   │   └── nodes.py
│   │
│   ├── agents/
│   │   ├── company_agent.py
│   │   ├── financial_agent.py
│   │   ├── media_agent.py
│   │   ├── industry_agent.py
│   │   ├── policy_agent.py
│   │   └── memo_agent.py
│   │
│   ├── tools/
│   │   ├── companies_house.py
│   │   ├── web_search.py
│   │   ├── ratio_calculator.py
│   │   ├── policy_engine.py
│   │   └── report_generator.py
│   │
│   ├── prompts/
│   │   ├── company_prompt.txt
│   │   ├── industry_prompt.txt
│   │   ├── media_prompt.txt
│   │   └── memo_prompt.txt
│   │
│   ├── models/
│   │   ├── schemas.py
│   │   └── output_models.py
│   │
│   ├── data/
│   │   ├── synthetic_credit_policy.json
│   │   ├── sector_mappings.json
│   │   └── test_cases.json
│   │
│   └── services/
│       ├── llm_service.py
│       ├── storage_service.py
│       └── logging_service.py
│
├── frontend/
│   ├── streamlit_app.py
│   └── components/
│
├── tests/
│   ├── test_ratios.py
│   ├── test_policy_engine.py
│   └── test_agents.py
│
└── docs/
    ├── architecture.md
    ├── workflow.md
    └── screenshots/