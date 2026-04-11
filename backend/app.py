from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .agents.runner import run_graph_stream

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    async def event_generator():
        async for msg in run_graph_stream(req.question):
            yield f"data: {msg}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
