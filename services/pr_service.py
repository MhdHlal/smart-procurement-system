from database.config import SessionLocal
from models.purchase_request import PurchaseRequest

def submit_purchase_request(pr_number, product_id, material_id, quantity, requester, requested_date, notes):
    session = SessionLocal()
    try:
        # إنشاء سجل طلب شراء جديد مع الحالة الابتدائية "Pending RFQ"
        new_pr = PurchaseRequest(
            pr_number=pr_number,
            product_id=product_id,
            material_id=material_id,
            quantity=quantity,
            requester_name=requester,
            requested_date=requested_date,
            notes=notes,
            status="Pending RFQ"  # الإضافة الأساسية لضمان تتبع دورة حياة الطلب
        )
        session.add(new_pr)
        session.commit()
        return True
    except Exception as e:
        # طباعة الخطأ بشكل مفصل تساعد الخبير الرقمي في التصحيح السريع
        print(f"Error submitting PR {pr_number}: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def get_all_products():
    from models.product import Product
    session = SessionLocal()
    try:
        return session.query(Product).all()
    finally:
        session.close()

def get_materials_for_product(product_id):
    from models.bom import BOM
    from models.material import RawMaterial
    session = SessionLocal()
    try:
        return session.query(RawMaterial, BOM.quantity_required).join(BOM).filter(BOM.product_id == product_id).all()
    finally:
        session.close()