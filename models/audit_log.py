from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database.config import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_email = Column(String(100), nullable=False) # من قام بالحركة؟
    action = Column(String(50), nullable=False)      # نوع الحركة (CREATE, UPDATE, DELETE)
    entity_type = Column(String(50))                 # أين تمت الحركة؟ (Vendor, RFQ, PR)
    details = Column(Text)                           # تفاصيل إضافية
    status = Column(String(20), default="Success")   # حالة الحركة