from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastmcp import Client
from typing import Optional
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


# Models
class ChatRequest(BaseModel):
    message: str
    filename: Optional[str] = None


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



# File upload endpoint

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "data"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": f"File {file.filename} uploaded successfully", "filename": file.filename}


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    reply = await process_user_message(
        user_input=req.message,
        mcp_client=app.state.mcp_client,
        filename=req.filename
    )
    return {"reply": reply}


# Serve frontend safely
# Mount frontend on /frontend to avoid conflicts with /upload or /chat
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
