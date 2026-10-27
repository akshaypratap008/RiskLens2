import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langgraph.types import Command

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

load_dotenv(project_root / ".env")

if not os.getenv("COMPANY_HOUSE_API"):
    st.error("COMPANY_HOUSE_API is missing. Check the project's .env file.")
    st.stop()

if not os.getenv("TAVILY_API_KEY"):
    st.error("TAVILY_API_KEY is missing. Check the project's .env file.")
    st.stop()

from risklens2.graph.workflow import workflow

import uuid


st.title("New Credit Analysis")
st.write(
    "Run company research, provide financial information, and generate "
    "the credit assessment."
)

company_number = st.session_state.get("company_number", "").strip()

if not company_number:
    st.warning("Enter a company number on the Home page before starting an analysis.")
    st.page_link("Home.py", label="Go to Home")
    st.stop()

st.caption(f"Company number: **{company_number}**")

if st.button("Start analysis", type="primary"):
    # A new thread keeps this analysis separate from previous submissions.
    st.session_state["workflow_config"] = {
        "configurable": {"thread_id": uuid.uuid4().hex}
    }
    st.session_state["workflow_result"] = None
    st.session_state["workflow_pending"] = False

    try:
        with st.spinner("Researching the company, industry, and adverse media…"):
            result = workflow.invoke(
                {"company_number": company_number},
                st.session_state["workflow_config"],
            )

        st.session_state["workflow_result"] = result
        st.session_state["workflow_pending"] = "__interrupt__" in result

        if not st.session_state["workflow_pending"]:
            st.success("Analysis completed.")
    except Exception as exc:
        st.error("The analysis could not be started.")
        st.exception(exc)

result = st.session_state.get("workflow_result")

if result:
    company_research = result.get("company_research")
    profile = getattr(company_research, "company_profile", None)

    if profile:
        st.subheader(getattr(profile, "company_name", "Company details"))
        st.write(f"**Status:** {getattr(profile, 'status', 'Not available')}")
        st.write(f"**Company type:** {getattr(profile, 'type', 'Not available')}")
        st.write(
            "**Industries:** "
            + ", ".join(getattr(profile, "industry_names", []) or [])
        )

if st.session_state.get("workflow_pending"):
    st.divider()
    st.subheader("Financial information")
    st.write("Enter the figures for the latest financial year to continue.")

    with st.form("financial_inputs"):
        left, right = st.columns(2)

        with left:
            revenue_cy = st.number_input(
                "Current-year revenue",
                min_value=0.01,
                value=1.0,
                help="Must be greater than zero.",
            )
            revenue_py = st.number_input(
                "Prior-year revenue",
                min_value=0.01,
                value=1.0,
                help="Must be greater than zero to calculate revenue growth.",
            )
            ebitda = st.number_input(
                "EBITDA",
                value=0.0,
                help="Must not be zero because it is used as a ratio denominator.",
            )
            net_profit = st.number_input("Net profit", value=0.0)
            cash = st.number_input("Cash", min_value=0.0, value=0.0)
            current_assets = st.number_input(
                "Current assets", min_value=0.0, value=0.0
            )
            inventory = st.number_input("Inventory", min_value=0.0, value=0.0)

        with right:
            current_liabilities = st.number_input(
                "Current liabilities",
                min_value=0.01,
                value=1.0,
                help="Must be greater than zero to calculate liquidity ratios.",
            )
            total_assets = st.number_input("Total assets", min_value=0.0, value=0.0)
            total_liabilities = st.number_input(
                "Total liabilities", min_value=0.0, value=0.0
            )
            equity = st.number_input(
                "Equity",
                min_value=0.01,
                value=1.0,
                help="Must be greater than zero to calculate debt-to-equity.",
            )
            total_debt = st.number_input("Total debt", min_value=0.0, value=0.0)
            interest_expense = st.number_input(
                "Interest expense",
                min_value=0.01,
                value=1.0,
                help="Must be greater than zero to calculate interest cover.",
            )

        submitted = st.form_submit_button(
            "Continue assessment",
            type="primary",
        )

    if submitted:
        if ebitda == 0:
            st.error("EBITDA must not be zero because it is used to calculate ratios.")
        else:
            financials = {
                "revenue_cy": revenue_cy,
                "revenue_py": revenue_py,
                "ebitda": ebitda,
                "net_profit": net_profit,
                "cash": cash,
                "current_assets": current_assets,
                "inventory": inventory,
                "current_liabilities": current_liabilities,
                "total_assets": total_assets,
                "total_liabilities": total_liabilities,
                "equity": equity,
                "total_debt": total_debt,
                "interest_expense": interest_expense,
            }

            try:
                with st.spinner("Calculating ratios and generating the credit memo…"):
                    completed_result = workflow.invoke(
                        Command(resume=financials),
                        st.session_state["workflow_config"],
                    )

                st.session_state["workflow_result"] = completed_result
                st.session_state["workflow_pending"] = (
                    "__interrupt__" in completed_result
                )

                if st.session_state["workflow_pending"]:
                    st.warning("The workflow requested additional input.")
                else:
                    st.success(
                        "Assessment completed. Open the Results page to review it."
                    )
            except Exception as exc:
                st.error("The assessment could not be completed.")
                st.exception(exc)