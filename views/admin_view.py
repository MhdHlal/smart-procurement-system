import streamlit as st
from models.product import Product
from models.material import RawMaterial
from models.bom import BOM
from models.vendor import Vendor
from sqlalchemy import Column, Integer, String, Text
from database.config import Base, engine
from models.quotation import Quotation
from models.rfq import RFQ
from services.logger_service import log_system_action
import os

# تعريف سريع لموديل الإعدادات لضمان وجود الجدول
class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True)
    company_name = Column(String, default="My Manufacturing Co.")
    company_email = Column(String, default="procurement@factory.com")
    company_web = Column(String, default="www.factory.com")
    payment_terms = Column(Text, default="Net 30 Days")
    delivery_terms = Column(Text, default="Ex-Works")
    currency = Column(String, default="USD")

def show_admin_view(session):
    # إنشاء جدول الإعدادات إذا لم يكن موجوداً
    Base.metadata.create_all(bind=engine)
    
    st.markdown("<h2 class='role-header'>⚙️ Master Data & Settings</h2>", unsafe_allow_html=True)
    t1, t2, t3, t4, t5 = st.tabs(["📦 Products", "🧪 Materials", "📋 BOM", "🏢 Settings", "🤝 Vendors"])
    
    with t1:
        with st.form("p_form", clear_on_submit=True):
            np = st.text_input("New Product Name")
            if st.form_submit_button("Add Product"): 
                if np: session.add(Product(name=np)); session.commit(); st.rerun()
        for p in session.query(Product).all():
            c1, c2, c3 = st.columns([4,1,1])
            edit_p = c1.text_input("P", p.name, key=f"p_{p.id}", label_visibility="collapsed")
            if c2.button("💾", key=f"u_{p.id}"): p.name = edit_p; session.commit(); st.rerun()
            if c3.button("🗑️", key=f"d_{p.id}"): 
                if not session.query(BOM).filter_by(product_id=p.id).first(): session.delete(p); session.commit(); st.rerun()
                else: st.error("Delete BOM first")

    with t2:
        unit_options = ["Kg", "Meters", "Units", "Liters"]
        with st.form("m_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            n, u = c1.text_input("Material Name"), c2.selectbox("Unit", unit_options)
            if st.form_submit_button("Add Material"):
                if n: session.add(RawMaterial(material_name=n, unit=u)); session.commit(); st.rerun()
        for m in session.query(RawMaterial).all():
            c1, c2, c3, c4 = st.columns([3,2,1,1])
            nm = c1.text_input("M", m.material_name, key=f"m_{m.id}", label_visibility="collapsed")
            try: current_unit_index = unit_options.index(m.unit)
            except: current_unit_index = 0
            un = c2.selectbox("U", unit_options, index=current_unit_index, key=f"un_{m.id}", label_visibility="collapsed")
            if c3.button("💾", key=f"mu_{m.id}"): 
                m.material_name, m.unit = nm, un
                session.commit(); st.success("Updated!"); st.rerun()
            if c4.button("🗑️", key=f"md_{m.id}"):
                if not session.query(BOM).filter_by(material_id=m.id).first(): session.delete(m); session.commit(); st.rerun()
                else: st.error("In use")

    with t3:
        prods, mats = session.query(Product).all(), session.query(RawMaterial).all()
        with st.form("b_form", clear_on_submit=True):
            c1,c2,c3 = st.columns(3)
            sp = c1.selectbox("Product", [p.name for p in prods]) if prods else None
            sm = c2.selectbox("Material", [m.material_name for m in mats]) if mats else None
            sq = c3.number_input("Qty Required", min_value=0.1)
            if st.form_submit_button("Link to BOM") and sp and sm:
                pid = next(p.id for p in prods if p.name == sp)
                mid = next(m.id for m in mats if m.material_name == sm)
                session.add(BOM(product_id=pid, material_id=mid, quantity_required=sq))
                session.commit(); st.rerun()
        for b in session.query(BOM).all():
            if b.product and b.material:
                c1,c2,c3,c4,c5 = st.columns([2,2,2,1,1])
                c1.write(f"**{b.product.name}**")
                c2.write(b.material.material_name)
                nq = c3.number_input("Q", value=float(b.quantity_required), key=f"bq_{b.id}", label_visibility="collapsed")
                if c4.button("💾", key=f"bu_{b.id}"): b.quantity_required = nq; session.commit(); st.rerun()
                if c5.button("🗑️", key=f"bd_{b.id}"): session.delete(b); session.commit(); st.rerun()

    with t4:
        st.subheader("Global RFQ Settings")
        # استخدام SQLAlchemy لإدارة الإعدادات بدلاً من التوصيل اليدوي
        setting = session.query(SystemSetting).filter_by(id=1).first()
        if not setting:
            setting = SystemSetting(id=1)
            session.add(setting)
            session.commit()

        with st.form("settings_form"):
            c1, c2 = st.columns(2)
            setting.company_name = c1.text_input("Company Name", value=setting.company_name)
            setting.company_email = c2.text_input("Public Email", value=setting.company_email)
            setting.company_web = c1.text_input("Website", value=setting.company_web)
            setting.currency = c2.text_input("Default Currency", value=setting.currency)
            setting.payment_terms = st.text_area("Default Payment Terms", value=setting.payment_terms)
            setting.delivery_terms = st.text_area("Default Delivery Terms", value=setting.delivery_terms)
            
            if st.form_submit_button("Update All Settings"):
                session.commit()
                st.success("✅ Settings updated successfully!")

    with t5:
        st.subheader("🏢 Manage Specialized Vendors")
        
        # جلب جميع المواد والموردين
        all_materials = session.query(RawMaterial).all()
        mat_options = {m.material_name: m.id for m in all_materials}
        inv_mat_options = {m.id: m.material_name for m in all_materials} # للبحث العكسي عن اسم المادة

        # --- القسم الأول: إضافة مورد جديد ---
        with st.expander("➕ Add New Vendor", expanded=False):
            with st.form("vendor_registration_form", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                vn = col1.text_input("Vendor Name")
                ve = col2.text_input("Vendor Email")
                v_spec = col3.selectbox("Specialization", list(mat_options.keys()) if mat_options else ["None"])
        
                if st.form_submit_button("Add Specialized Vendor", type="primary"):
                    if vn and ve and mat_options:
                        try:
                            # 1. العملية الأساسية: إضافة المورد
                            new_vendor = Vendor(name=vn, email=ve, material_specialty_id=mat_options[v_spec])
                            session.add(new_vendor)
                            session.commit()
                    
                            # 2. زرع المستشعر: تسجيل الحركة في سجل الرقابة
                            # نستخدم الإيميل من ملف .env لتمثيل الشخص الذي قام بالإجراء
                            log_system_action(
                                user_email=os.getenv("SENDER_EMAIL", "Admin_User"),
                                action="CREATE",
                                entity_type="Vendor",
                                details=f"Added new vendor: {vn} ({ve}) specialized in {v_spec}"
                            )

                            st.toast(f"✅ Added {vn} successfully!")
                            st.rerun()
                        except Exception as e:
                            session.rollback() # تراجع عن العملية في حال حدوث خطأ
                            st.error(f"❌ Failed to add vendor: {str(e)}")
                    else:
                        st.error("⚠️ Please fill all fields.")

        st.markdown("---")
        
        # --- القسم الثاني: تعديل أو حذف الموردين الحاليين ---
        st.markdown("#### 🛠️ Edit or Delete Vendors")
        all_vendors = session.query(Vendor).all()
        
        if not all_vendors:
            st.info("ℹ️ No vendors available in the system.")
        else:
            # تجهيز قائمة بأسماء الموردين لتسهيل الاختيار
            vendor_dict = {f"{v.name} ({v.email})": v for v in all_vendors}
            selected_vendor_label = st.selectbox("🔍 Select Vendor to Manage", list(vendor_dict.keys()))
            
            if selected_vendor_label:
                target_v = vendor_dict[selected_vendor_label]
                
                # استخدام form لضمان عدم تنفيذ التعديلات إلا عند الضغط على الزر
                with st.form(f"edit_vendor_form_{target_v.id}"):
                    c1, c2, c3 = st.columns(3)
                    
                    new_name = c1.text_input("Name", value=target_v.name)
                    new_email = c2.text_input("Email", value=target_v.email)
                    
                    # --- 1. معالجة خطأ التخصص المفقود (Safe Indexing) ---
                    current_mat_name = inv_mat_options.get(target_v.material_specialty_id, "None")
                    mat_list = list(mat_options.keys())
                    
                    default_index = 0
                    if mat_list and current_mat_name != "None":
                        try:
                            default_index = mat_list.index(current_mat_name)
                        except ValueError:
                            # إذا تم حذف المادة من قاعدة البيانات سابقاً
                            st.warning("⚠️ The material assigned to this vendor no longer exists. Please assign a new one.")
                            default_index = 0
                    
                    new_spec = c3.selectbox("Specialization", mat_list if mat_list else ["None"], index=default_index)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    col_upd, col_del = st.columns([1, 1])
                    
                    update_btn = col_upd.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                    delete_btn = col_del.form_submit_button("🗑️ Delete Vendor", use_container_width=True)
                    
                    if update_btn:
                        old_info = f"{target_v.name} ({target_v.email})"
                        target_v.name = new_name
                        target_v.email = new_email
                        if mat_options:
                            target_v.material_specialty_id = mat_options[new_spec]
                        session.commit()
                        log_system_action(
                            user_email=os.getenv("SENDER_EMAIL", "Admin"),
                            action="UPDATE",
                            entity_type="Vendor",
                            details=f"Modified vendor info from [{old_info}] to [{new_name} ({new_email})]"
                        )
                        st.toast(f"✅ Vendor '{new_name}' updated!", icon="💾")
                        st.rerun()
                        
                    # --- 2. الحماية قبل الحذف (Foreign Key Safety) ---
                    if delete_btn:
                        # أ. فحص هل المورد مرتبط بعروض أسعار مسجلة؟
                        has_quotes = session.query(Quotation).filter_by(vendor_id=target_v.id).first()
                        
                        # ب. فحص هل المورد تم اختياره في طلبات RFQ سابقة؟
                        has_rfqs = False
                        all_rfqs = session.query(RFQ).all()
                        for r in all_rfqs:
                            if r.selected_vendor_ids and str(target_v.id) in r.selected_vendor_ids.split(","):
                                has_rfqs = True
                                break
                        
                        if has_quotes or has_rfqs:
                            # في حال الرفض، نسجل محاولة حذف فاشلة لزيادة الرقابة
                            log_system_action(
                                user_email=os.getenv("SENDER_EMAIL", "Admin"),
                                action="SECURITY_ALERT",
                                entity_type="Vendor",
                                details=f"Attempted to delete active vendor [{target_v.name}] but was blocked by system constraints.",
                                status="Failed"
                            )
                            # منع الحذف وعرض رسالة توجيهية
                            st.error(f"⛔ Cannot delete '{target_v.name}'. This vendor is linked to existing RFQs or Quotations. To disable them, rename the vendor to 'DO NOT USE - {target_v.name}'.")
                        else:
                            # السماح بالحذف إذا كان المورد جديداً ولم يستخدم في أي عملية
                            try:
                                v_name_deleted = target_v.name
                                session.delete(target_v)
                                session.commit()
                                log_system_action(
                                    user_email=os.getenv("SENDER_EMAIL", "Admin"),
                                    action="DELETE",
                                    entity_type="Vendor",
                                    details=f"Permanently deleted vendor: {v_name_deleted}"
                                )
                                st.toast("🗑️ Vendor permanently deleted.", icon="✅")
                                st.rerun()
                            except Exception as e:
                                session.rollback() # التراجع عن أي تغيير معلق في حال حدوث خطأ
                                st.error(f"❌ Database Error: {str(e)}")