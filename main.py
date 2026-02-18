import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
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
def chat(payload: ChatIn):
    response = client.responses.create(
        model="gpt-4.1",
        input=payload.user_input
    )
    return {"response": response.output_text}
