from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime

class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    pr_id = Column(Integer, ForeignKey("purchase_requests.id")) 
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    
    # السعر المقدم من المورد
    price = Column(Float, nullable=False)
    
    # تحديد العرض الفائز بناءً على قاعدة "أقل سعر"
    is_awarded = Column(Boolean, default=False)
    
    received_at = Column(DateTime, default=datetime.utcnow)

    # العلاقات لتسهيل الوصول للبيانات في واجهة المقارنة
    vendor = relationship("Vendor")
    pr = relationship("PurchaseRequest", back_populates="quotations")