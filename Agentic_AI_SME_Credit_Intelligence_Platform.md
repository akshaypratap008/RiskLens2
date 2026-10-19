# Agentic AI SME Credit Intelligence Platform

## Project Goal

Build a multi-agent AI system that helps a commercial credit analyst perform SME due diligence and generate a structured credit assessment.

The project is NOT intended to automatically approve or decline credit.

Instead, it acts as an AI-powered Credit Analyst Copilot that gathers information, performs analysis, highlights risks, and generates a professional credit memo.

---

# Why This Project

The original concept focused heavily on:

- Company filing extraction
- Bankruptcy prediction
- Policy evaluation

The challenge is that filing extraction becomes the dominant engineering problem because Companies House filings are submitted in multiple formats with inconsistent structures.

To keep the project realistic and focused on Agentic AI, financial statement extraction should NOT be a dependency for Version 1.

The project should demonstrate:

- Multi-agent orchestration
- Tool usage
- Information gathering
- Reasoning
- Report generation
- Human-in-the-loop workflows

---

# High-Level Architecture

User
│
├── Company Name
├── Basic Financial Inputs
│
▼
Orchestrator Agent
│
├── Agent 1: Company Research Agent
├── Agent 2: Financial Analysis Agent
├── Agent 3: Adverse Media Agent
├── Agent 4: Industry Intelligence Agent
├── Agent 5: Credit Policy Agent
│
▼
Credit Memo Agent
│
▼
Final Due Diligence Report

---

# User Journey

## Recommended User Flow

User enters:

```text
Analyse ABC Foods Ltd
```

System automatically gathers:

- Company information
- Director details
- SIC code
- Charges
- Company age
- Industry information
- Adverse media information

System then asks user for:

```text
Revenue
EBITDA
Cash
Debt
Current Assets
Current Liabilities
Interest Expense
```

User provides financial data.

Agents execute.

Final report is produced.

---

# Agent 1 - Company Research Agent

## Objective

Build a company profile.

## Inputs

Company name.

## Data Sources

### Companies House API

Collect:

- Company Number
- Company Name
- Incorporation Date
- Company Status
- SIC Codes
- Registered Office
- Directors
- PSCs (Persons with Significant Control)
- Filing History
- Charges

### Company Website

Collect:

- Company description
- Products and services
- Markets served
- Customer segments

## Outputs

```json
{
  "company_name": "ABC Foods Ltd",
  "incorporation_year": 2014,
  "sic_code": "10850",
  "industry": "Food Manufacturing",
  "directors": 2,
  "charges": 3,
  "status": "Active"
}
```

## LLM Involvement

Low.

Mostly deterministic retrieval and summarisation.

---

# Agent 2 - Financial Analysis Agent

## Objective

Calculate financial ratios and identify strengths and weaknesses.

## Inputs

User-provided financials.

Example:

```json
{
  "revenue": 15000000,
  "ebitda": 1200000,
  "cash": 400000,
  "debt": 2500000,
  "current_assets": 3200000,
  "current_liabilities": 2200000
}
```

## Version 1 Rule

Do NOT depend on automatically extracting financial statements.

Manual input is acceptable.

## Metrics Calculated

### Profitability

- EBITDA Margin
- Net Margin
- Revenue Growth

### Liquidity

- Current Ratio
- Quick Ratio
- Working Capital

### Leverage

- Debt / EBITDA
- Debt / Equity
- Net Debt / EBITDA

### Coverage

- Interest Cover
- DSCR

## Outputs

```json
{
  "current_ratio": 1.45,
  "debt_to_ebitda": 2.1,
  "interest_cover": 4.7
}
```

## LLM Involvement

Medium.

Narrative explanation of strengths and weaknesses.

---

# Agent 3 - Adverse Media Agent

## Objective

Identify reputational, financial crime, regulatory and insolvency risks.

## Inputs

- Company Name
- Director Names

## Search Keywords

Combine company and director names with:

- fraud
- insolvency
- liquidation
- administration
- sanctions
- money laundering
- regulatory fine
- director disqualification
- investigation

## Sources

### GOV.UK

- Insolvency Service
- Director disqualifications

### FCA

- Regulatory actions
- Warnings

### Companies House

- Dissolved companies
- Insolvency filings

### General News Search

- National newspapers
- Trade press
- Regional news

## Outputs

```json
{
  "risk_found": true,
  "severity": "Medium",
  "reason": "Director associated with dissolved company"
}
```

## LLM Involvement

High.

Used for summarisation and classification.

---

# Agent 4 - Industry Intelligence Agent

## Objective

Provide industry context.

## Inputs

- SIC Code
- Industry Name

## Sources

### Office for National Statistics (ONS)

- Growth trends
- Sector statistics

### Bank of England

- Interest rates
- Economic outlook

### UK Government Publications

- Industry reports
- Regulatory updates

### Industry Bodies

Examples:

- Food and Drink Federation
- British Retail Consortium
- Construction Leadership Council
- Logistics UK

### Professional Services Firms

- PwC
- EY
- KPMG
- Deloitte

## Outputs

```json
{
  "industry_outlook": "Stable",
  "key_risks": [
    "Commodity inflation",
    "Labour shortages"
  ]
}
```

## LLM Involvement

High.

Used to synthesize multiple sources.

---

# Agent 5 - Credit Policy Agent

## Objective

Evaluate company metrics against the synthetic credit policy.

## Inputs

- Ratios generated by Agent 2
- Policy thresholds

## Evaluation Type

Rule Engine.

Not RAG.

Not primarily LLM-based.

Examples:

```python
if current_ratio < 1.0:
    fail
```

```python
if debt_to_ebitda > 3.0:
    refer
```

## Outputs

```json
{
  "passed_rules": 18,
  "failed_rules": 2,
  "decision": "REFER"
}
```

## LLM Involvement

Low.

Only for explanation.

---

# Credit Memo Agent

## Objective

Transform structured outputs from all agents into a professional credit report.

## Inputs

- Company Profile
- Financial Analysis
- Policy Findings
- Industry Analysis
- Adverse Media Results

## Output Structure

### Executive Summary

### Business Overview

### Financial Assessment

### Strengths

### Weaknesses

### Industry Risks

### Adverse Media Findings

### Policy Assessment

### Recommendation

Possible outcomes:

- Approve
- Refer
- Decline

## LLM Involvement

Very High.

This is the primary report-generation component.

---

# Agent Orchestration Flow

```text
User
 │
 ├── Company Name
 ├── Financial Inputs
 │
 ▼
 Orchestrator
 │
 ├── Financial Analysis Agent
 ├── Credit Policy Agent
 ├── Company Research Agent
 ├── Adverse Media Agent
 ├── Industry Intelligence Agent
 │
 ▼
 Credit Memo Agent
 │
 ▼
 Final Due Diligence Report
```

---

# Recommended Technology Stack

## LLM Framework

- LangGraph (preferred)
- CrewAI

## LLMs

- GPT-5
- Azure OpenAI

## Backend

- Python
- FastAPI

## Data Validation

- Pydantic

## Storage

- PostgreSQL
- SQLite (initial version)

## Frontend

- Streamlit

---

# Future Enhancements

## Version 2

Add automated financial extraction:

- Companies House
- iXBRL
- Dataledger

## Version 3

Add:

- PD model
- Risk grade prediction
- Portfolio monitoring

## Version 4

Add:

- Conversational analyst workflow
- Credit committee simulation
- Multi-agent debate mechanism

---

# Success Criteria

A successful Version 1 should:

1. Accept company name plus financials.
2. Gather company information automatically.
3. Identify adverse media.
4. Generate ratio analysis.
5. Assess policy compliance.
6. Produce a professional credit memo.
7. Demonstrate genuine multi-agent collaboration.

Focus on completing Version 1 before attempting filing extraction or bankruptcy prediction.
