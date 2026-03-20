from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.config import Base

class RawMaterial(Base):
    __tablename__ = "raw_materials"
    id = Column(Integer, primary_key=True, index=True)
    material_name = Column(String, unique=True)
    unit = Column(String)
    
    products = relationship("BOM", back_populates="material")
