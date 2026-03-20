from sqlalchemy import Column, Integer, String, ForeignKey
from database.config import Base

class Vendor(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    # ربط المورد بمادة محددة من جدول المواد الخام
    material_specialty_id = Column(Integer, ForeignKey('raw_materials.id'))