from database.config import engine, SessionLocal
from models import Base, Product, RawMaterial, BOM

def initialize_system():
    # 1. Create all tables in the database
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    
    try:
        # Check if data already exists to avoid duplication
        if session.query(Product).count() == 0:
            print("Seeding initial master data...")
            
            # Add Products
            p_a = Product(name="Product A")
            p_b = Product(name="Product B")
            p_c = Product(name="Product C")
            session.add_all([p_a, p_b, p_c])
            session.flush() # Flush to get IDs
            
            # Add Raw Materials
            m1 = RawMaterial(material_name="Steel Sheet", unit="Kg")
            m2 = RawMaterial(material_name="Plastic Pellets", unit="Kg")
            m3 = RawMaterial(material_name="Copper Wire", unit="Meters")
            session.add_all([m1, m2, m3])
            session.flush()
            
            # Add BOM (Recipe)
            # Product A needs 10.5 Kg Steel and 5 Kg Plastic
            bom1 = BOM(product_id=p_a.id, material_id=m1.id, quantity_required=10.5)
            bom2 = BOM(product_id=p_a.id, material_id=m2.id, quantity_required=5.0)
            # Product B needs 20 Meters Copper
            bom3 = BOM(product_id=p_b.id, material_id=m3.id, quantity_required=20.0)
            
            session.add_all([bom1, bom2, bom3])
            session.commit()
            print("? Database initialized and seeded successfully.")
        else:
            print("?? Database already contains data. Skipping seeding.")
            
    except Exception as e:
        print(f"? Error during initialization: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    initialize_system()
