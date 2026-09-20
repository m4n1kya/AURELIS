import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

import sys
import os

# Ensure the 'engine' directory is on the path so we can import the core logic
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'engine'))

from api.aurelis_service import AurelisService

app = FastAPI(title="AURELIS API Bridge")

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
def health_check():
    return {"status": "ok", "engine": "deterministic"}

@app.get("/api/requests")
def list_requests() -> List[Dict[str, Any]]:
    """Returns a list of all request IDs and base metadata."""
    try:
        return service.get_all_requests()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analyze/{request_id}")
def analyze_request(request_id: str) -> Dict[str, Any]:
    """Runs the deterministic evaluator for a specific request and returns a structured payload."""
    try:
        return service.analyze(request_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
