from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime

class RFQ(Base):
    __tablename__ = "rfqs"
    
    id = Column(Integer, primary_key=True, index=True)
    rfq_number = Column(String, unique=True, index=True)
    pr_id = Column(Integer, ForeignKey("purchase_requests.id"))
    
    vendor_instructions = Column(String)
    
    # NEW FIELD: Store selected vendor IDs as a comma-separated string
    selected_vendor_ids = Column(String) 
    
    deadline = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow) 

    pr = relationship("PurchaseRequest", back_populates="rfq")