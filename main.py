from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
from agent import handle_customer_message
from database import DB_FILE

app = FastAPI(title="MantraYudha Support Agent")

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ResetRequest(BaseModel):
    session_id: str

@app.get("/api/health")
async def health_endpoint():
    return {"status": "healthy"}

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        # Using customer_id=1 as a default for the MVP
        result = handle_customer_message(conn, 1, req.message)
        conn.close()
        
        # Ensure the response matches what the frontend expects
        return {
            "decision": result.get("decision", "ANSWER"),
            "reply": result.get("message", ""),
            "intents": [],
            "events": [{"type": "thought", "detail": "Processed message from agent"}],
            "actions": [],
            "fallback": False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset")
async def reset_endpoint(req: ResetRequest):
    return {"status": "ok", "message": "Session reset"}

# Mount the static directory at the root last
app.mount("/", StaticFiles(directory="static", html=True), name="static")
