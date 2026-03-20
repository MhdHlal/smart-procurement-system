from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime

class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    pr_number = Column(String, unique=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    material_id = Column(Integer, ForeignKey("raw_materials.id"))
    quantity = Column(Float)
    requester_name = Column(String, nullable=False)
    requested_date = Column(String)  # يمكن لاحقاً تحويله لـ Date لمرونة أكبر
    notes = Column(String)
    
    # التعديل الاحترافي: حالات الطلب تتبع دورة الحياة الرقمية
    # الحالات المتوقعة: "Pending RFQ", "RFQ Sent", "Quotes Received", "Closed"
    status = Column(String, default="Pending RFQ")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # العلاقات (Relationships)
    product = relationship("Product")
    material = relationship("RawMaterial")
    
    # علاقة مع جدول الـ RFQ (واحد لواحد)
    rfq = relationship("RFQ", back_populates="pr", uselist=False)
    
    # الإضافة الجديدة: علاقة مع جدول عروض الأسعار (واحد لمتعدد)
    # سننشئ ملف quotation.py تالياً ليعمل هذا الرابط
    quotations = relationship("Quotation", back_populates="pr")