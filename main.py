import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
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
