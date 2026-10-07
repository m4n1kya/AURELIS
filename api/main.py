"""
AURELIS API Bridge
==================

This module provides the FastAPI application that serves as the bridge between the 
Next.js frontend and the core deterministic AURELIS engine. It exposes endpoints 
for health checks, listing requests, and running deep financial analysis on a 
specific request.
"""

import sys
import os
import time
import logging
from typing import List, Dict, Any

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

# Ensure the 'engine' directory is on the path so we can import the core logic
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'engine'))

from api.aurelis_service import AurelisService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthResponse(BaseModel):
    status: str
    engine: str

app = FastAPI(title="AURELIS API Bridge")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Path: {request.url.path} completed in {process_time:.4f}s")
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Configure CORS to allow the Next.js frontend to communicate securely with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = AurelisService()

@app.get("/api/health")
def health_check() -> HealthResponse:
    return {"status": "ok", "engine": "deterministic"}

@app.get("/api/requests")

# Endpoint definitions
def list_requests() -> List[Dict[str, Any]]:
    """Returns a list of all request IDs and base metadata."""
    try:
        return service.get_all_requests()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analyze/{request_id}")
def analyze_request(request_id: str = __import__('fastapi').Path(..., title="The ID of the request to analyze")) -> Dict[str, Any]:
    """Runs the deterministic evaluator for a specific request and returns a structured payload."""
    try:
        return service.analyze(request_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
