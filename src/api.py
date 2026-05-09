from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
import os

from .agent.graph import GRAPH
from .agent.state import DEFAULT_STATE

app = FastAPI(title="SocrAItes API")

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_path):
    os.makedirs(static_path)

app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    socratic_depth: Optional[int] = 1
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    retrieved_docs: List[Any] = []
    plan: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Prepare state for LangGraph
        initial_messages = [{"role": m.role, "content": m.content} for m in request.messages]
        
        state = DEFAULT_STATE.copy()
        state.update({
            "messages": initial_messages,
            "socratic_depth": request.socratic_depth,
        })
        
        # Execute Graph
        # Note: GRAPH.compile() is needed if not already compiled
        runnable = GRAPH.compile()
        result = runnable.invoke(state)
        
        return ChatResponse(
            answer=result.get("draft_answer", "I'm sorry, I couldn't formulate a response."),
            session_id=session_id,
            retrieved_docs=result.get("retrieved_docs", []),
            plan=result.get("plan")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
