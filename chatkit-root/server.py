# server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI

# --- CONFIG ---
WORKFLOW_ID = "wf_6900a7a0713c8190842ed336a668b4a506103a3f5b4a4b4a"  # <- your workflow id
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # set this in your server env
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in environment before starting the server")

# --- APP ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production (e.g., ["https://your-framer-site.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai = OpenAI(api_key=OPENAI_API_KEY)

class SessionRequest(BaseModel):
    deviceId: str | None = None

@app.post("/api/chatkit/session")
async def create_chatkit_session(req: SessionRequest | None = None):
    """
    Creates a ChatKit session on the server and returns the client_secret
    The front-end uses this client_secret to initialize the ChatKit widget.
    """
    device_id = (req.deviceId if req else None) or "anonymous-" + os.urandom(6).hex()
    try:
        # Adjust payload as needed per OpenAI ChatKit API
        session = openai.chatkit.sessions.create({
            "workflow": {"id": WORKFLOW_ID},
            "user": device_id
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create chatkit session: {e}")

    # session.client_secret is the secret your frontend will use directly
    return {"client_secret": session.client_secret}

# Run with: uvicorn server:app --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
