from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessageGraph
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")



class State(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]


model=ChatOpenAI(temperature=0)


def make_invoce_agent_graph():
    """Make a tool-calling agent"""

    @tool
    def cal__state_tax(base_price: float, tax_rate: float) -> float:
        """Calculate state tax to the base price.

        Args:
            base_price: The price before tax.
            tax_rate: Tax rate in percentage.
        """
        return (base_price * tax_rate / 100)
    @tool
    def cal__country_tax(base_price: float, tax_rate: float) -> float:
        """Calculate country tax to the base price.

        Args:
            base_price: The price before tax.
            tax_rate: Tax rate in percentage.
        """
        return  (base_price * tax_rate / 100)
    @tool
    def add_final__tax(base_price: float, stateTax: float,countryTax:float) -> float:
        """Add  state tax,country tax to the base price and return the final tax.

        Args:
            base_price: The price before tax.
            stateTax: state tax
            countryTax: country tax
        """
        return base_price + stateTax+countryTax

    @tool
    def apply_discount(taxedPrice: float, discount_percent: float) -> float:
        """Apply discount to the taxedPrice.

        Args:
            taxedPrice: The taxedPrice before discount.
            discount_percent: Discount percentage to apply.
        """
        return taxedPrice - (taxedPrice * discount_percent / 100)


    tool_node = ToolNode([cal__state_tax,cal__country_tax,add_final__tax,apply_discount])
    model_with_tools = model.bind_tools([cal__state_tax,cal__country_tax,add_final__tax,apply_discount])
    def call_model(state):
        return {"messages": [model_with_tools.invoke(state["messages"])]}

    def should_continue(state: State):
        if state["messages"][-1].tool_calls:
            return "tools"
        else:
            return END

    graph_workflow = StateGraph(State)

    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_node("tools", tool_node)
    graph_workflow.add_edge(START, "agent")
    graph_workflow.add_conditional_edges("agent", should_continue)
    graph_workflow.add_edge("tools", "agent")

    agent = graph_workflow.compile()
    return agent

agent=make_invoce_agent_graph()