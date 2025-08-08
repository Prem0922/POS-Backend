from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func
from database import Base

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
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(String) 