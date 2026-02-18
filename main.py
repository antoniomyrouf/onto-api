import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi import Header
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔥 CORS DOIT ÊTRE AJOUTÉ JUSTE APRÈS FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://anima-omnia.com",
        "https://www.anima-omnia.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatIn(BaseModel):
    user_input: str

@app.get("/")
def root():
    return {"message": "Onto API is running"}

@app.post("/chat")
def chat(
    payload: ChatIn,
    x_onto_key: str | None = Header(default=None)
):
    uid = payload.user_id or "public"
    text = payload.user_input.strip()
    return {"response": onto_reply(text, user_id=uid, pro_key=x_onto_key)}

