from .state import GraphState
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import sys
from datetime import datetime
from langchain_openai import ChatOpenAI
from .planner import planner_node
from .executor import executor_node
from .synthesizer import synthesizer_node

graph = StateGraph(GraphState)

graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("synthesizer", synthesizer_node)

graph.set_entry_point("planner")

graph.add_edge("planner", "executor")
graph.add_edge("executor", "synthesizer")
graph.add_edge("synthesizer", END)

app = graph.compile()

if __name__ == "__main__":
    #question = "How much interest income did I earn?" # fact only
    #question = "What is interest income on a 1099-INT?" # explanation only
    question = "What is interest income on a 1099-INT and how much did I earn?" # fact + explanation


    initial_state: GraphState = {
        "question": question,
        "plan": None,
        "fact_results": None,
        "explainer_docs": None,
        "answer": None
    }

    final_state = app.invoke(initial_state)

    print("Final Answer:")
    print(final_state["answer"])


  




