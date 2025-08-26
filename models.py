from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.sql import func
from database import Base

class POSUser(Base):
    __tablename__ = "pos_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default="cashier")  # cashier, manager, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))

class POSLog(Base):
    __tablename__ = "pos_logs"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    card_id = Column(String, index=True)
    customer_id = Column(String, index=True)
    amount = Column(String)
    status = Column(String)
    transaction_id = Column(String, index=True)
    robot_run_id = Column(String, index=True)
    user_id = Column(Integer, index=True)  # Track which POS user performed the operation
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(String) 