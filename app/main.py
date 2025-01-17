from dotenv import load_dotenv, find_dotenv
import os
from fastapi import FastAPI
from pydantic import BaseModel
from app.helpers.gemini_chat import gemini_chat
from app.helpers.gemini_embedding import gemini_embedding
from app.helpers.split_text_recursive import split_text_recursive
from app.notes.create import create
from app.notes.semantic_search import semantic_search
from app.temp_kb import temp_kb
from app.notes.rag_answer import rag_answer
from app.helpers.sqlite_db import init_db, get_all_notes as get_all


load_dotenv(find_dotenv())

from app.helpers.sqlite_db import init_db

app = FastAPI()

# Initialize the SQLite database
init_db()


@app.get("/ping", tags=["Health Check"])
async def ping():
    return {"message": "pong"}


class ChatMessage(BaseModel):
    user_message: str


@app.post("/chat", tags=["Chat"])
async def chat(reqbody: ChatMessage):
    try:
        ai_response = await gemini_chat(reqbody.user_message, temp_kb)
        return {"message": ai_response}
    except Exception as e:
        print(e)
        return {
            "message": "Sorry, I'm having trouble processing your request. Please try again later."
        }


@app.post("/get-embedding", tags=["Embedding"])
async def get_embedding(reqbody: ChatMessage):
    embedding = await gemini_embedding(reqbody.user_message)
    length = len(embedding)
    return {"message": embedding, "length": length}


@app.post("/test-split-text", tags=["Text Split"])
async def test_split_text(reqbody: ChatMessage):
    result = split_text_recursive(reqbody.user_message)
    return {"data": result}


class CreateNotes(BaseModel):
    note: str


@app.post("/notes", tags=["Notes"])
async def create_notes(reqbody: CreateNotes):
    note = reqbody.note
    created = await create(note)
    return {"data": created}


@app.get("/notes/", tags=["Notes"])
async def get_all_notes():
    notes = get_all()
    return {"data": notes}


class GetSimilarNotes(BaseModel):
    text: str


@app.get("/notes/get-similar", tags=["Notes"])
async def get_similar_notes(text: str):
    notes = await semantic_search(text)
    return {"data": notes}


@app.get("/rag-chat", tags=["RAG-Chat"])
async def rag_chat(text: str):
    answer = await rag_answer(text)
    return {"data": answer}
