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
from api import router

load_dotenv()

app = FastAPI(
    title="POS Backend API",
    description="Point of Sale Backend API for fare media operations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")

CRM_BASE_URL = os.getenv("CRM_BASE_URL", "https://crm-n577.onrender.com")
CRM_API_KEY = os.getenv("CRM_API_KEY", "mysecretkey")

class StandardResponse:
    def __init__(self, status: str, message: str, data: Optional[dict] = None, robotRunId: Optional[str] = None):
        self.status = status
        self.timestamp = datetime.utcnow()
        self.transactionId = str(uuid.uuid4())
        self.robotRunId = robotRunId
        self.message = message
        self.data = data

    def dict(self):
        return {
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
            "transactionId": self.transactionId,
            "robotRunId": self.robotRunId,
            "message": self.message,
            "data": self.data
        }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

API_KEY = os.getenv("POS_API_KEY", "pos_secret_key")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

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

@app.post("/api/cards/issue")
async def issue_card(
    card_data: dict,
    robotRunId: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = make_crm_request("/cards/issue", "POST", card_data)
        
        response = StandardResponse(
            status="success",
            message="Card issued successfully",
            data=result,
            robotRunId=robotRunId
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            message=f"Failed to issue card: {str(e)}",
            robotRunId=robotRunId
        )
        return response.dict()

@app.post("/api/cards/{card_id}/reload")
async def reload_card(
    card_id: str,
    reload_data: dict,
    robotRunId: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = make_crm_request(f"/cards/{card_id}/reload", "POST", reload_data)
        
        response = StandardResponse(
            status="success",
            message="Card reloaded successfully",
            data=result,
            robotRunId=robotRunId
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            message=f"Failed to reload card: {str(e)}",
            robotRunId=robotRunId
        )
        return response.dict()

@app.post("/api/cards/{card_id}/products")
async def add_product(
    card_id: str,
    product_data: dict,
    robotRunId: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = make_crm_request(f"/cards/{card_id}/products", "POST", product_data)
        
        response = StandardResponse(
            status="success",
            message="Product added successfully",
            data=result,
            robotRunId=robotRunId
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            message=f"Failed to add product: {str(e)}",
            robotRunId=robotRunId
        )
        return response.dict()

@app.get("/api/cards/{card_id}/balance")
async def get_card_balance(
    card_id: str,
    robotRunId: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = make_crm_request(f"/cards/{card_id}/balance")
        
        response = StandardResponse(
            status="success",
            message="Card balance retrieved successfully",
            data=result,
            robotRunId=robotRunId
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            message=f"Failed to get card balance: {str(e)}",
            robotRunId=robotRunId
        )
        return response.dict()

@app.post("/api/payment/simulate")
async def simulate_payment(
    payment_data: dict,
    robotRunId: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = make_crm_request("/payment/simulate", "POST", payment_data)
        
        response = StandardResponse(
            status="success",
            message="Payment simulated successfully",
            data=result,
            robotRunId=robotRunId
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            message=f"Failed to simulate payment: {str(e)}",
            robotRunId=robotRunId
        )
        return response.dict()

@app.get("/api/customers/{customer_id}")
async def get_customer(
    customer_id: str,
    robotRunId: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = make_crm_request(f"/customers/{customer_id}")
        
        response = StandardResponse(
            status="success",
            message="Customer information retrieved successfully",
            data=result,
            robotRunId=robotRunId
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            message=f"Failed to get customer: {str(e)}",
            robotRunId=robotRunId
        )
        return response.dict()

@app.get("/api/cards/{card_id}/transactions")
async def get_card_transactions(
    card_id: str,
    robotRunId: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = make_crm_request(f"/cards/{card_id}/transactions")
        
        response = StandardResponse(
            status="success",
            message="Card transactions retrieved successfully",
            data=result,
            robotRunId=robotRunId
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            message=f"Failed to get card transactions: {str(e)}",
            robotRunId=robotRunId
        )
        return response.dict()

@app.get("/api/reports/summary")
async def get_reports_summary(
    robotRunId: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = make_crm_request("/reports/summary")
        
        response = StandardResponse(
            status="success",
            message="Reports summary retrieved successfully",
            data=result,
            robotRunId=robotRunId
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            message=f"Failed to get reports summary: {str(e)}",
            robotRunId=robotRunId
        )
        return response.dict()

@app.post("/api/simulate/cardTap")
async def simulate_card_tap(
    tap_data: dict,
    robotRunId: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = make_crm_request("/simulate/cardTap", "POST", tap_data)
        
        response = StandardResponse(
            status="success",
            message="Card tap simulated successfully",
            data=result,
            robotRunId=robotRunId
        )
        return response.dict()
    except Exception as e:
        response = StandardResponse(
            status="error",
            message=f"Failed to simulate card tap: {str(e)}",
            robotRunId=robotRunId
        )
        return response.dict()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "POS Backend", "timestamp": datetime.utcnow().isoformat()}

@app.get("/")
async def root():
    return {
        "message": "POS Backend API",
        "version": "1.0.0",
        "endpoints": [
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