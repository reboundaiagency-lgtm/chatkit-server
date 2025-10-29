# server.py  <-- replace your root entrypoint with this exact file
from fastapi import FastAPI, Request
from openai import OpenAI
import os, traceback

app = FastAPI()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "openai_key_present": bool(OPENAI_API_KEY),
        "entrypoint": "server.py"
    }

@app.post("/api/chatkit/session")
async def create_chatkit_session(request: Request):
    try:
        if client is None:
            return {"error": "OPENAI_API_KEY missing"}
        body = {}
        try:
            body = await request.json()
        except:
            body = {}
        user = body.get("user", "visitor")
        print("DEBUG create session for user:", user)
        session = client.chatkit.sessions.create(
            workflow={"id": "wf_6900a7a0713c8190842ed336a668b4a506103a3f5b4a4b4a"},
            user=user
        )
        print("DEBUG got session:", hasattr(session, "client_secret"))
        return {"client_secret": session.client_secret}
    except Exception as e:
        tb = traceback.format_exc()
        print("ERROR:", e)
        print(tb)
        return {"error": "server_exception", "message": str(e)}
