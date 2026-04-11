import json
from typing import AsyncGenerator
from .multiagent import app
from .state import GraphState

async def run_graph_stream(question: str) -> AsyncGenerator[str, None]:
    initial_state: GraphState = {
        "question": question,
        "plan": None,
        "fact_results": None,
        "explainer_docs": None,
        "answer": None,
        "trace": []
    }

    async for event in app.astream(initial_state, stream_mode="values"):
        # event is the updated state after each node runs
        if "trace" in event and event["trace"]:
            yield json.dumps({
                "type": "trace",
                "trace": event["trace"][-1]
            })

        if "answer" in event and event["answer"]:
            yield json.dumps({
                "type": "answer",
                "answer": event["answer"]
            })

    yield json.dumps({"type": "done"})
