from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastmcp import Client
from typing import Optional
import os
import uvicorn

from llm_agent import process_user_message

MCP_SERVER_URL = "http://127.0.0.1:8080/mcp"

app = FastAPI(title="File Assistant Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models
class ChatResponse(BaseModel):
    reply: str


# MCP client setup
@app.on_event("startup")
async def startup():
    app.state.mcp_client = Client(MCP_SERVER_URL)
    await app.state.mcp_client.__aenter__()


@app.on_event("shutdown")
async def shutdown():
    await app.state.mcp_client.__aexit__(None, None, None)


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(message: str = Form(...), file: Optional[UploadFile] = File(None)):
    file_path_for_llm = None
    if file:
        upload_dir = "data"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        file_path_for_llm = file_path

    reply = await process_user_message(
        user_input=message,
        mcp_client=app.state.mcp_client,
        filename=file_path_for_llm
    )
    return {"reply": reply}


# Serve frontend safely
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
