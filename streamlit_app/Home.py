import streamlit as st


st.set_page_config(
    page_title="RiskLens2",
    page_icon="📊",
    layout="wide",
)

st.title("RiskLens2")
st.subheader("SME Credit Intelligence Platform")

st.write(
    "Assess a company's profile, financial performance, policy fit, and "
    "adverse media in one place."
)

st.markdown(
    """
    **To begin:** enter a company number in the sidebar and select
    **Start new analysis**. You can then provide financial information and
    review the resulting assessment.
    """
)

# Initialize shared state for the multipage app.
st.session_state.setdefault("company_number", "")
st.session_state.setdefault("workflow_result", None)
st.session_state.setdefault("workflow_pending", False)

with st.sidebar:
    st.header("Company")

    with st.form("company_selection"):
        company_number = st.text_input(
            "Company number",
            value=st.session_state["company_number"],
            placeholder="e.g. 12345678",
        )
        submitted = st.form_submit_button(
            "Start new analysis",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        company_number = company_number.strip()

        if not company_number:
            st.error("Enter a company number to continue.")
        else:
            st.session_state["company_number"] = company_number
            st.session_state["workflow_result"] = None
            st.session_state["workflow_pending"] = False
            st.session_state.pop("workflow_config", None)

            st.switch_page("pages/1_New_Analysis.py")