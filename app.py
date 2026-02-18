from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastmcp import Client
import asyncio
import os
import uvicorn

from llm_agent import process_user_message

MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

app = FastAPI(title="File Assistant Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str


@app.on_event("startup")
async def startup():
    app.state.mcp_client = Client(MCP_SERVER_URL)
    await app.state.mcp_client.__aenter__()


@app.on_event("shutdown")
async def shutdown():
    await app.state.mcp_client.__aexit__(None, None, None)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "data"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    return {"message": f"File {file.filename} uploaded successfully", "filename": file.filename}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    reply = await process_user_message(
        user_input = req.message,
        mcp_client = app.state.mcp_client
    )
    return {"reply": reply}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
