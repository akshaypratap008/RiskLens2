from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver

from src.risklens2.graph.state import CreditState
from src.risklens2.graph.nodes import company_research, industry_research, media_research, get_financials_input, financial_analysis, policy_assessment, credit_memo


graph = StateGraph(state_schema=CreditState)

graph.add_node("company_research", company_research)
graph.add_node("industry_research", industry_research)
graph.add_node("media_research", media_research)
graph.add_node("get_financials_input", get_financials_input)
graph.add_node("financial_analysis", financial_analysis)
graph.add_node("policy_assessment", policy_assessment)
graph.add_node("credit_memo", credit_memo)

graph.add_edge(START, "company_research")

# parralel nodes
graph.add_edge("company_research", "industry_research")
graph.add_edge("company_research", "media_research")
graph.add_edge("industry_research", "get_financials_input")
graph.add_edge("media_research", "get_financials_input")

graph.add_edge("get_financials_input", "financial_analysis")
graph.add_edge("financial_analysis", "policy_assessment")
graph.add_edge("policy_assessment", "credit_memo")
graph.add_edge("credit_memo", END)

workflow = graph.compile(checkpointer= InMemorySaver())










