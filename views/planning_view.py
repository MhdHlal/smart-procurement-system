import streamlit as st
import os
from datetime import datetime
from models.product import Product
from models.bom import BOM
from services.pr_service import submit_purchase_request
from services.logger_service import log_system_action

def show_planning_view(session):
    st.markdown("<h2 class='role-header'>🛒 Planning: Create Purchase Request</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        pr_num = st.text_input("PR Number", value=f"PR-{datetime.now().strftime('%M%S')}")
        req_name = st.text_input("Requester Name", value="Planning Dept")
        req_date = st.date_input("Requested Date")
        notes = st.text_area("Internal Notes (Optional)")
        
        # جلب المنتجات المتاحة
        prods = session.query(Product).all()
        prod_map = {p.name: p.id for p in prods}
        sel_prod = st.selectbox("Select Product to Produce", [""] + list(prod_map.keys())) if prod_map else None
    
    with col2:
        if sel_prod and sel_prod != "":
            # جلب المواد الخام بناءً على الـ BOM للمنتج المختار
            bom_items = session.query(BOM).filter_by(product_id=prod_map[sel_prod]).all()
            
            if bom_items:
                mat_map = {f"{b.material.material_name} ({b.material.unit})": (b.material_id, b.quantity_required) 
                           for b in bom_items if b.material}
                
                sel_mat_label = st.selectbox("Raw Material Required", list(mat_map.keys()))
                mat_id, std_qty = mat_map[sel_mat_label]
                
                qty = st.number_input("Order Quantity", value=float(std_qty), min_value=0.1)
                
                st.markdown("<br><br>", unsafe_allow_html=True)
                
                # إرسال الطلب
                if st.button("🚀 Submit PR to Purchasing", type="primary", width='stretch'):
                    # التعديل هنا: تأكد أن الأسماء تطابق ما هو موجود في pr_service.py
                    success = submit_purchase_request(
                        pr_number=pr_num,      # تأكد أنها pr_number وليس pr_num
                        product_id=prod_map[sel_prod], 
                        material_id=mat_id, 
                        quantity=qty, 
                        requester=req_name,    # تأكد أنها requester
                        requested_date=req_date.strftime("%Y-%m-%d"), 
                        notes=notes
                    )
                    
                    if success:
                        log_system_action(
                            user_email=os.getenv("SENDER_EMAIL", "Planning_Dept"),
                            action="CREATE_PR",
                            entity_type="Planning",
                            details=f"Created PR #{pr_num} for product [{sel_prod}]. Material: {sel_mat_label}, Qty: {qty}."
                        )
                        st.success(f"✅ {pr_num} Created successfully and marked as 'Pending RFQ'!")
                        st.info("The Purchasing Team can now view and process this request.")
                    else:
                        log_system_action(
                            user_email=os.getenv("SENDER_EMAIL", "Planning_Dept"),
                            action="PR_FAILURE",
                            entity_type="Planning",
                            details=f"Failed to create PR #{pr_num}. Check pr_service logs.",
                            status="Failed"
                        )
                        st.error("❌ Failed to submit PR. Please check system logs.")
            else:
                st.warning("⚠️ No Bill of Materials (BOM) defined for this product.")