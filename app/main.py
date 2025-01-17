import os
from fastapi import FastAPI
from pydantic import BaseModel
from app.helpers.gemini_chat import gemini_chat
from app.helpers.gemini_embedding import gemini_embedding
from app.temp_kb import temp_kb

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "pong"}


class ChatMessage(BaseModel):
    user_message: str


@app.post("/chat")
async def chat(reqbody: ChatMessage):
    try:
        ai_response = await gemini_chat(reqbody.user_message, temp_kb)
        return {"message": ai_response}
    except Exception as e:
        print(e)
        return {
            "message": "Sorry, I'm having trouble processing your request. Please try again later."
        }


@app.post("/get-embedding")
async def get_embedding(reqbody: ChatMessage):
    embedding = await gemini_embedding(reqbody.user_message)
    length = len(embedding)
    return {"message": embedding, "length": length}
