from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.phase_3_retrieval.engine import FactualFAQAssistant

app = FastAPI(title="Mutual Fund FAQ API")

# Configure CORS for Vercel Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Assistant
# Global instance for the API
try:
    assistant = FactualFAQAssistant()
except Exception as e:
    print(f"Error initializing assistant: {e}")
    assistant = None

# Request/Response Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    last_updated: str

class FundInfo(BaseModel):
    name: str
    category: str
    risk: str
    expense_ratio: str
    min_sip: str
    image_url: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "online", "message": "Mutual Fund FAQ API is running"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not assistant:
        raise HTTPException(status_code=500, detail="Assistant not initialized")
    
    try:
        result = assistant.query(request.message)
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            last_updated=result["last_updated"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/funds", response_model=List[FundInfo])
def get_funds():
    # Hardcoded metadata to match the high-fidelity UI requirements
    # and the funds we actually track.
    return [
        {
            "name": "HDFC Mid Cap Fund",
            "category": "Equity: Mid Cap",
            "risk": "Very High",
            "expense_ratio": "0.77%",
            "min_sip": "₹1,000"
        },
        {
            "name": "HDFC Equity Fund",
            "category": "Equity: Multi Cap",
            "risk": "Very High",
            "expense_ratio": "0.85%",
            "min_sip": "₹500"
        },
        {
            "name": "HDFC Focused Fund",
            "category": "Equity: Focused",
            "risk": "Very High",
            "expense_ratio": "0.95%",
            "min_sip": "₹1,000"
        },
        {
            "name": "HDFC ELSS Tax Saver Fund",
            "category": "Equity: ELSS",
            "risk": "Very High",
            "expense_ratio": "0.91%",
            "min_sip": "₹500"
        },
        {
            "name": "HDFC Large Cap Fund",
            "category": "Equity: Large Cap",
            "risk": "Very High",
            "expense_ratio": "0.89%",
            "min_sip": "₹1,000"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
