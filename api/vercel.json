from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.post("/api/chatkit/session")
async def create_chatkit_session():
    session = client.chatkit.sessions.create(
        workflow={"id": "wf_6900a7a0713c8190842ed336a668b4a506103a3f5b4a4b4a"},
        user="visitor"
    )
    return {"client_secret": session.client_secret}
