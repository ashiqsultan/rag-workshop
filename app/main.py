from dotenv import load_dotenv, find_dotenv
import os
from fastapi import FastAPI
from pydantic import BaseModel


load_dotenv(find_dotenv())


app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "pong"}


class ChatMessage(BaseModel):
    user_message: str


@app.post("/chat")
async def chat(reqbody: ChatMessage):
    return {"message": "Hello this is test. This is your message: " + reqbody.user_message}


@app.get("/app-name")
async def get_app_name():
    app_name = os.getenv("APP_NAME", "DefaultAppName")
    return {"app_name": app_name}
