from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base

class BOM(Base):
    __tablename__ = "bom"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    material_id = Column(Integer, ForeignKey("raw_materials.id"))
    quantity_required = Column(Float)

    product = relationship("Product", back_populates="materials")
    material = relationship("RawMaterial", back_populates="products")
