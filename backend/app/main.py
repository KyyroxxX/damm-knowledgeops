import os
import boto3
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from mangum import Mangum

from app.rag_engine import retrieve_relevant_chunks
from app.assistant import ask_industrial_assistant
from app.incidents import router as incidents_router
from app.training import router as training_router
from app.proposals import router as proposals_router

app = FastAPI(
    title="Damm KnowledgeOps API",
    version="1.0.0",
    description="API empresarial de gestion del conocimiento industrial para Damm - MetropolisFPLab"
)

app.include_router(incidents_router)
app.include_router(training_router)
app.include_router(proposals_router)

security = HTTPBearer()

class ChatQueryRequest(BaseModel):
    query: str
    department: str = "general"

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "damm-knowledgeops-api"}

@app.get("/api/v1/auth/me")
def get_user_profile(credentials: HTTPAuthorizationCredentials = Security(security)):
    return {"message": "Authenticated successfully"}

@app.post("/api/v1/chat/query")
def chat_query(data: ChatQueryRequest):
    approved_keys = ["vectors/test_manual.json"]
    bucket_name = os.environ.get("PROCESSED_BUCKET", "")
    chunks = retrieve_relevant_chunks(data.query, approved_keys, bucket_name, top_k=3)
    response = ask_industrial_assistant(data.query, chunks)
    return response

handler = Mangum(app)
