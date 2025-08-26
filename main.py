from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid
import os
import requests
from dotenv import load_dotenv

from database import SessionLocal, engine
from models import Base
from auth import get_current_active_user, get_db
from auth_router import router as auth_router
from schemas import StandardResponse

# Load environment variables
load_dotenv()

app = FastAPI(
    title="POS Backend API",
    description="Point of Sale Backend API for fare media operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Include the authentication router
app.include_router(auth_router, prefix="/api")

# CRM Backend URL for data operations
CRM_BASE_URL = os.getenv("CRM_BASE_URL", "https://crm-n577.onrender.com")
CRM_API_KEY = os.getenv("CRM_API_KEY", "mysecretkey")

# Helper function to make requests to CRM backend
def make_crm_request(endpoint: str, method: str = "GET", data: dict = None):
    url = f"{CRM_BASE_URL}{endpoint}"
    headers = {
        "x-api-key": CRM_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"CRM backend error: {str(e)}")

# POS API Endpoints - Now using JWT authentication

@app.post("/api/cards/issue")
async def issue_card(
    card_data: dict,
    robotRunId: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Issue a new card"""
    try:
        # Call CRM backend to issue card
        result = make_crm_request("/cards/issue", "POST", card_data)
        
        response = StandardResponse(
            status="success",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message="Card issued successfully",
            data=result
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message=f"Failed to issue card: {str(e)}"
        )
        return response.dict()

@app.post("/api/cards/{card_id}/reload")
async def reload_card(
    card_id: str,
    reload_data: dict,
    robotRunId: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Reload card with amount"""
    try:
        # Call CRM backend to reload card
        result = make_crm_request(f"/cards/{card_id}/reload", "POST", reload_data)
        
        response = StandardResponse(
            status="success",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message="Card reloaded successfully",
            data=result
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message=f"Failed to reload card: {str(e)}"
        )
        return response.dict()

@app.post("/api/cards/{card_id}/products")
async def add_product(
    card_id: str,
    product_data: dict,
    robotRunId: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add product to card"""
    try:
        # Call CRM backend to add product
        result = make_crm_request(f"/cards/{card_id}/products", "POST", product_data)
        
        response = StandardResponse(
            status="success",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message="Product added successfully",
            data=result
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message=f"Failed to add product: {str(e)}"
        )
        return response.dict()

@app.get("/api/cards/{card_id}/balance")
async def get_card_balance(
    card_id: str,
    robotRunId: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get card balance"""
    try:
        # Call CRM backend to get card balance
        result = make_crm_request(f"/cards/{card_id}/balance")
        
        response = StandardResponse(
            status="success",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message="Card balance retrieved successfully",
            data=result
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message=f"Failed to get card balance: {str(e)}"
        )
        return response.dict()

@app.post("/api/payment/simulate")
async def simulate_payment(
    payment_data: dict,
    robotRunId: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Simulate payment"""
    try:
        # Call CRM backend to simulate payment
        result = make_crm_request("/payment/simulate", "POST", payment_data)
        
        response = StandardResponse(
            status="success",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message="Payment simulated successfully",
            data=result
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message=f"Failed to simulate payment: {str(e)}"
        )
        return response.dict()

@app.get("/api/customers/{customer_id}")
async def get_customer(
    customer_id: str,
    robotRunId: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get customer information"""
    try:
        # Call CRM backend to get customer
        result = make_crm_request(f"/customers/{customer_id}")
        
        response = StandardResponse(
            status="success",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message="Customer information retrieved successfully",
            data=result
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message=f"Failed to get customer: {str(e)}"
        )
        return response.dict()

@app.get("/api/cards/{card_id}/transactions")
async def get_card_transactions(
    card_id: str,
    robotRunId: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get card transaction history"""
    try:
        # Call CRM backend to get card transactions
        result = make_crm_request(f"/cards/{card_id}/transactions")
        
        response = StandardResponse(
            status="success",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message="Card transactions retrieved successfully",
            data=result
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message=f"Failed to get card transactions: {str(e)}"
        )
        return response.dict()

@app.get("/api/reports/summary")
async def get_reports_summary(
    robotRunId: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get reports summary"""
    try:
        # Call CRM backend to get reports summary
        result = make_crm_request("/reports/summary")
        
        response = StandardResponse(
            status="success",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message="Reports summary retrieved successfully",
            data=result
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message=f"Failed to get reports summary: {str(e)}"
        )
        return response.dict()

@app.post("/api/simulate/cardTap")
async def simulate_card_tap(
    tap_data: dict,
    robotRunId: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Simulate card tap"""
    try:
        # Call CRM backend to simulate card tap
        result = make_crm_request("/simulate/cardTap", "POST", tap_data)
        
        response = StandardResponse(
            status="success",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message="Card tap simulated successfully",
            data=result
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            timestamp=datetime.utcnow(),
            transactionId=str(uuid.uuid4()),
            robotRunId=robotRunId,
            message=f"Failed to simulate card tap: {str(e)}"
        )
        return response.dict()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "POS Backend", "timestamp": datetime.utcnow().isoformat()}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "POS Backend API",
        "version": "1.0.0",
        "authentication": "JWT Bearer Token Required",
        "endpoints": [
            "POST /api/auth/signup",
            "POST /api/auth/login", 
            "GET /api/auth/me",
            "POST /api/auth/refresh",
            "POST /api/auth/logout",
            "POST /api/cards/issue",
            "POST /api/cards/{id}/reload", 
            "POST /api/cards/{id}/products",
            "GET /api/cards/{id}/balance",
            "POST /api/payment/simulate",
            "GET /api/customers/{id}",
            "GET /api/cards/{id}/transactions",
            "GET /api/reports/summary",
            "POST /api/simulate/cardTap"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 