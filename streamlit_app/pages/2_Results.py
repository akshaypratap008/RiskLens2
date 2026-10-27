import pandas as pd
import streamlit as st


st.title("Credit Assessment Results")

result = st.session_state.get("workflow_result")

if not result:
    if st.session_state.get("workflow_pending"):
        st.info("The assessment is waiting for financial inputs.")
        st.page_link("pages/1_New_Analysis.py", label="Continue analysis")
    else:
        st.info("No completed assessment is available yet.")
        st.page_link("pages/1_New_Analysis.py", label="Start a new analysis")
    st.stop()


def to_dict(value):
    """Convert Pydantic models and mappings into displayable dictionaries."""
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, dict):
        return value
    return None


def show_data(value):
    data = to_dict(value)
    if data is not None:
        st.json(data, expanded=True)
    elif value is None:
        st.info("No data available.")
    else:
        st.write(value)


def show_metric_group(title, values, percent_fields=()):
    st.markdown(f"#### {title}")
    if not values:
        st.info("No metrics available.")
        return

    items = list(values.items())
    for start in range(0, len(items), 3):
        columns = st.columns(3)
        for column, (name, value) in zip(columns, items[start : start + 3]):
            label = name.replace("_", " ").title()
            if value is None:
                display_value = "N/A"
            elif name in percent_fields:
                display_value = f"{value * 100:.2f}%"
            elif isinstance(value, (int, float)):
                display_value = f"{value:,.2f}"
            else:
                display_value = str(value)
            column.metric(label, display_value)


company_name = result.get("company_name") or "Company assessment"
st.caption(f"Results for **{company_name}**")

tabs = st.tabs(
    [
        "Executive Summary",
        "Company Profile",
        "Financial Analysis",
        "Policy Assessment",
        "Adverse Media Info",
        "Credit Memo",
    ]
)

with tabs[0]:
    st.subheader("Executive Summary")

    policy = to_dict(result.get("policy_assessment")) or {}
    recommendation = policy.get("recomendation") or policy.get("recommendation")

    if recommendation:
        st.metric("Policy recommendation", recommendation)

    financial_analysis = to_dict(result.get("financial_analysis")) or {}
    profitability = financial_analysis.get("profitability") or {}
    revenue_growth = profitability.get("revenue_growth")
    if revenue_growth is not None:
        st.metric("Revenue growth", f"{revenue_growth:.2f}%")

    company_research = to_dict(result.get("company_research")) or {}
    profile = company_research.get("company_profile") or {}
    if profile:
        st.markdown("#### Company overview")
        st.write(f"**Name:** {profile.get('company_name', 'Not available')}")
        st.write(f"**Company number:** {profile.get('company_number', 'Not available')}")
        st.write(f"**Status:** {profile.get('status', 'Not available')}")
        industries = profile.get("industry_names") or []
        st.write(f"**Industries:** {', '.join(industries) or 'Not available'}")

    industry_analysis = result.get("industry_analysis")
    if industry_analysis:
        st.markdown("#### Industry analysis")
        show_data(industry_analysis)


with tabs[1]:
    st.subheader("Company Profile")
    research = to_dict(result.get("company_research")) or {}
    profile = research.get("company_profile")

    if profile:
        profile = to_dict(profile) or profile
        st.json(profile, expanded=True)

        for section_name, key in (
            ("Directors and officers", "director_details"),
            ("Persons with significant control", "psc_details"),
            ("Filings", "filing_details"),
            ("Insolvency", "insolvency_details"),
            ("Charges", "charges_details"),
        ):
            section = research.get(key)
            with st.expander(section_name):
                show_data(section)
    else:
        st.info("Company profile information is not available.")


with tabs[2]:
    st.subheader("Financial Analysis")
    financial_analysis = to_dict(result.get("financial_analysis"))

    if financial_analysis:
        show_metric_group(
            "Profitability",
            financial_analysis.get("profitability", {}),
            percent_fields={"ebitda_margin", "net_margin"},
        )
        show_metric_group("Liquidity", financial_analysis.get("liquidity", {}))
        show_metric_group("Leverage", financial_analysis.get("leverage", {}))
        show_metric_group("Coverage", financial_analysis.get("coverage", {}))

        with st.expander("Full financial analysis data"):
            st.json(financial_analysis, expanded=True)
    else:
        st.info("Financial analysis is not available.")


with tabs[3]:
    st.subheader("Policy Assessment")
    policy = to_dict(result.get("policy_assessment"))

    if policy:
        recommendation = policy.get("recomendation") or policy.get("recommendation")
        if recommendation:
            st.metric("Recommendation", recommendation)

        for title, key in (
            ("Passed rules", "passed_rules"),
            ("Failed rules", "failed_rules"),
        ):
            rules = policy.get(key) or []
            st.markdown(f"#### {title} ({len(rules)})")
            if rules:
                rows = [
                    to_dict(rule) or rule
                    for rule in rules
                ]
                st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
            else:
                st.write("None.")
    else:
        st.info("Policy assessment is not available.")


with tabs[4]:
    st.subheader("Adverse Media Information")
    media = to_dict(result.get("media_analysis"))

    if media:
        for title, key in (
            ("Company media", "company_adverse_media"),
            ("Director media", "director_adverse_media"),
        ):
            entries = media.get(key) or []
            st.markdown(f"#### {title} ({len(entries)})")

            if entries:
                rows = [to_dict(entry) or entry for entry in entries]
                st.dataframe(
                    pd.DataFrame(rows),
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "url": st.column_config.LinkColumn("Source"),
                    },
                )
            else:
                st.write("No items reported.")
    else:
        st.info("Adverse media information is not available.")


with tabs[5]:
    st.subheader("Credit Memo")
    memo = result.get("credit_memo")

    if memo:
        if isinstance(memo, str):
            st.markdown(memo)
        else:
            show_data(memo)
    else:
        st.info("Credit memo is not available.")