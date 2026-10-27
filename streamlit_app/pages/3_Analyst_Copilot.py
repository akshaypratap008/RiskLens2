import streamlit as st

st.title("Analyst Copilot")
st.caption("Chat interface — assistant functionality not connected yet.")

if "copilot_messages" not in st.session_state:
    st.session_state["copilot_messages"] = []

for message in st.session_state["copilot_messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a question about the credit assessment")

if prompt:
    st.session_state["copilot_messages"].append(
        {"role": "user", "content": prompt}
    )
    st.session_state["copilot_messages"].append(
        {
            "role": "assistant",
            "content": "Analyst Copilot is not connected yet.",
        }
    )
    st.rerun()