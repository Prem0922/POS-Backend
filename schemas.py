from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str = "cashier"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None

# POS Operation schemas
class CardIssueRequest(BaseModel):
    customer_id: str
    card_type: str = "standard"
    initial_balance: float = 0.0

class CardReloadRequest(BaseModel):
    amount: float
    payment_method: str = "cash"

class ProductAddRequest(BaseModel):
    product_id: str
    quantity: int = 1

class PaymentSimulateRequest(BaseModel):
    card_id: str
    amount: float
    fare_type: str = "standard"

class CardTapRequest(BaseModel):
    card_id: str
    station_id: str
    direction: str = "in"

# Response schemas
class StandardResponse(BaseModel):
    status: str
    timestamp: datetime
    transactionId: str
    robotRunId: Optional[str] = None
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    status: str
    timestamp: datetime
    transactionId: str
    message: str
    error_code: Optional[str] = None
