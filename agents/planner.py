from typing import TypedDict, Optional, List, Literal
from .prompts.agent_prompts import PLANNER_PROMPT
from .state import GraphState, ToolPlan
from dotenv import load_dotenv
import sys
from datetime import datetime
from langchain_openai import ChatOpenAI
import json

sys.path.append('../')
load_dotenv()   

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)



def planner_node(state: GraphState) -> GraphState:
    chain = PLANNER_PROMPT | llm
    response = chain.invoke({
        "question":state["question"]
    })
    # print("Planner Response:")

    plan_dict = json.loads(response.content)

    # print(plan_dict)

    plan = ToolPlan(**plan_dict)

    trace = state.get("trace", [])
    trace.append({
        "node": "planner",
        "decision": plan_dict
    })


    return {
        **state,
        "plan": plan,
        "trace": trace
    }
