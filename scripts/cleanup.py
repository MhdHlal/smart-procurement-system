from database.config import SessionLocal
from models.bom import BOM
from models.product import Product
from models.material import RawMaterial

session = SessionLocal()
# Delete BOMs that point to non-existent products or materials
boms = session.query(BOM).all()
for b in boms:
    if not b.product or not b.material:
        session.delete(b)
session.commit()
session.close()
print('? Database Cleaned!')
