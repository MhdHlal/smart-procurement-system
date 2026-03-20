from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.config import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # نستخدم اسم الكائن كنص 'BOM' لتجنب أخطاء الترتيب
    materials = relationship("BOM", back_populates="product")
