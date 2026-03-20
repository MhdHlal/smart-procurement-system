from database.config import Base, engine
from .product import Product
from .material import RawMaterial
from .bom import BOM
from .purchase_request import PurchaseRequest
from .rfq import RFQ

# أمر إنشاء الجداول فور تحميل الموديلات
Base.metadata.create_all(bind=engine)
