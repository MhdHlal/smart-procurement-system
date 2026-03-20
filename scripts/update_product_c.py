from database.config import SessionLocal
from models.product import Product
from models.material import RawMaterial
from models.bom import BOM

session = SessionLocal()
product_c = session.query(Product).filter_by(name="Product C").first()
copper = session.query(RawMaterial).filter_by(material_name="Copper Wire").first()

if product_c and copper:
    # Check if BOM already exists to avoid duplicates
    existing = session.query(BOM).filter_by(product_id=product_c.id, material_id=copper.id).first()
    if not existing:
        new_bom = BOM(product_id=product_c.id, material_id=copper.id, quantity_required=15.0)
        session.add(new_bom)
        session.commit()
        print("? BOM for Product C added successfully!")
    else:
        print("?? BOM for Product C already exists.")
session.close()
