from __future__ import annotations

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from onto_core.engine import onto_reply, prompt_hash

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://anima-omnia.com",
        "https://www.anima-omnia.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatIn(BaseModel):
    user_input: str
    user_id: str | None = None

@app.get("/")
def root():
    return {"message": "Onto API is running"}

@app.get("/version")
def version():
    return {"prompt_hash": prompt_hash()}

@app.post("/chat")
def chat(payload: ChatIn, x_onto_key: str | None = Header(default=None)):
    uid = payload.user_id or "public"
    text = payload.user_input.strip()
    return {"response": onto_reply(text, user_id=uid, pro_key=x_onto_key)}
