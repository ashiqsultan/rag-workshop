import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/get_app_name")
async def get_app_name():
    appname = os.getenv("APP_NAME", "default-fastapi-rag")
    return {"app_name": appname}