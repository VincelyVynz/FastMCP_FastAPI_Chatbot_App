from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastmcp import Client
import asyncio

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

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    reply = await process_user_message(
        user_input = req.message,
        mcp_client = app.state.mcp_client
    )
    return {"reply": reply}