import streamlit as st
import os
import pandas as pd
from datetime import datetime
from models.purchase_request import PurchaseRequest
from models.rfq import RFQ
from models.vendor import Vendor
from models.quotation import Quotation
from utils.pdf_generator import generate_rfq_pdf
from services.email_service import send_rfq_email
import os
from services.logger_service import log_system_action

def show_purchasing_view(session, ARCHIVE_DIR):
    st.markdown("<h2 class='role-header'>📄 Purchasing Management System</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🆕 New Requests (Pending RFQ)", "⚖️ Comparison & Awarding"])

    # --- Tab 1: Processing New RFQs ---
    with tab1:
        pending = session.query(PurchaseRequest).filter_by(status="Pending RFQ").all()
        if not pending:
            st.info("✅ No new purchase requests to process.")
        else:
            for pr in pending:
                with st.expander(f"📦 PR: {pr.pr_number} | Material: {pr.material.material_name}", expanded=True):
                    st.write(f"🔢 **Qty:** {pr.quantity} {getattr(pr.material, 'unit', '')} | 📅 **PR Date:** {pr.requested_date}")

                    if pr.notes:
                        st.info(f"📝 **Internal Notes (Planning):** {pr.notes}")

                    c1, c2 = st.columns(2)
                    rfq_no = c1.text_input("Assign RFQ ID", value=f"RFQ-{pr.pr_number.split('-')[-1]}", key=f"r_{pr.id}")
                    deadline = c2.date_input("Quotation Due Date", key=f"dt_{pr.id}")

                    instr = st.text_area("Vendor Instructions (Included in PDF only)", key=f"in_{pr.id}")

                    specialized_vendors = session.query(Vendor).filter_by(material_specialty_id=pr.material_id).all()
                    vendor_map = {f"{v.name} ({v.email})": v for v in specialized_vendors}

                    if not vendor_map:
                        st.warning("⚠️ No specialized vendors found.")
                        selected_vendors = []
                    else:
                        select_all = st.checkbox("Select All Vendors", key=f"chk_{pr.id}")
                        ms_key = f"ms_{pr.id}_{select_all}"
                        default_selection = list(vendor_map.keys()) if select_all else []
                        selected_labels = st.multiselect("Select Target Vendors", options=list(vendor_map.keys()), default=default_selection, key=ms_key)
                        selected_vendors = [vendor_map[l] for l in selected_labels]

                    # --- التعديل هنا: إضافة زر الأرشفة بجانب زر المعالجة ---
                    col_btn1, col_btn2 = st.columns([3, 1]) # تقسيم المساحة لزر كبير وزر صغير

                    with col_btn1:
                        if st.button("🚀 Process & Send RFQ", key=f"proc_{pr.id}", type="primary", width='stretch'):
                                if not selected_vendors:
                                    st.error("⚠️ Please select at least one vendor.")
                                    st.stop()

                                try:
                                    instr.encode('latin-1')
                                except UnicodeEncodeError:
                                    st.error("⚠️ FORMAT ERROR: Instructions must be in English only.")
                                    st.stop()

                                # --- التعديل: تغليف العمليات الثقيلة بمؤشر التحميل ---
                                with st.spinner("⏳ Generating PDF and sending emails... Please wait."):
                                    try:
                                        v_ids_str = ",".join([str(v.id) for v in selected_vendors])
                                        new_rfq = RFQ(
                                            rfq_number=rfq_no, 
                                            pr=pr,
                                            vendor_instructions=instr,
                                            selected_vendor_ids=v_ids_str,
                                            deadline=datetime.combine(deadline, datetime.min.time())
                                        )

                                        path = os.path.join(ARCHIVE_DIR, f"{rfq_no}.pdf")
                                        generate_rfq_pdf(new_rfq, path)

                                        pr.status = "RFQ Sent"
                                        session.add(new_rfq)
                                        session.commit()

                                        for v in selected_vendors:
                                            send_rfq_email(to_email=v.email, subject=f"RFQ: {rfq_no}", body="Please find attached our RFQ.", attachment_path=path)
                                        # --- 4. زرع مستشعر الرقابة (بعد نجاح جميع العمليات) ---
                                        log_system_action(
                                            user_email=os.getenv("SENDER_EMAIL", "Purchasing_Dept"),
                                            action="SEND_RFQ",
                                            entity_type="RFQ System",
                                            details=f"Issued RFQ: {rfq_no} for PR ID: {pr.id}. Total vendors notified: {len(selected_vendors)}."
                                        )
                                        # --- التعديل: إضافة التنبيه اللحظي قبل إعادة التحميل ---
                                        st.toast(f"✅ RFQ {rfq_no} sent successfully!", icon="🚀")
                                        st.rerun()
                                        
                                    except Exception as e:
                                        # في حال حدوث خطأ، نسجل المحاولة الفاشلة أيضاً للرقابة التقنية
                                        log_system_action(
                                            user_email=os.getenv("SENDER_EMAIL", "Purchasing_Dept"),
                                            action="RFQ_FAILURE",
                                            entity_type="RFQ System",
                                            details=f"Failed to process RFQ: {rfq_no}. Error: {str(e)}",
                                            status="Failed"
                                        )
                                        st.error(f"❌ System Error: {str(e)}")

                    with col_btn2:
                        # زر الأرشفة لتنظيف القائمة من الطلبات غير المرغوب فيها
                        if st.button("📁 Archive", key=f"arch_{pr.id}", width='stretch', help="Hide this request without processing"):
                            try:
                                pr_no = pr.pr_number
                                project_name = pr.project_name if hasattr(pr, 'project_name') else "Unknown Project"
                                pr.status = "Archived"
                                session.commit()
                                log_system_action(
                                    user_email=os.getenv("SENDER_EMAIL", "Purchasing_Dept"),
                                    action="ARCHIVE",
                                    entity_type="Purchase Request",
                                    details=f"Archived PR #{pr_no} for Project: {project_name}. Request was removed from active list."
                                )
                                st.warning(f"PR {pr.pr_number} Archived.")
                                st.rerun()
                            except Exception as e:
                                # تسجيل محاولة الأرشفة الفاشلة في حال وجود خطأ تقني
                                log_system_action(
                                    user_email=os.getenv("SENDER_EMAIL", "Purchasing_Dept"),
                                    action="ARCHIVE_FAIL",
                                    entity_type="Purchase Request",
                                    details=f"Failed to archive PR #{pr.pr_number}. Error: {str(e)}",
                                    status="Failed"
                                )
                                st.error(f"Error: {str(e)}")

    # --- Tab 2: Dynamic Comparison & Awarding ---
    with tab2:
        sent_requests = session.query(PurchaseRequest).filter_by(status="RFQ Sent").all()
        if not sent_requests:
            st.info("ℹ️ No requests are currently out for quotation.")
        else:
            for pr in sent_requests:
                with st.expander(f"⚖️ Awarding Process: {pr.pr_number} ({pr.material.material_name})"):
                    # --- ADDED: Display Planning Notes here as well for context during awarding ---
                    if pr.notes:
                        st.info(f"📝 **Internal Notes (Planning):** {pr.notes}")
                        
                    st.write(f"**RFQ Number:** {pr.rfq.rfq_number} | **Deadline:** {pr.rfq.deadline.date()}")
                    
                    if pr.rfq.selected_vendor_ids:
                        invited_ids = [int(i) for i in pr.rfq.selected_vendor_ids.split(",")]
                        invited_vendors = session.query(Vendor).filter(Vendor.id.in_(invited_ids)).all()
                    else:
                        invited_vendors = []

                    st.markdown("#### 📥 Enter Quotations Received")
                    
                    quote_entries = []
                    for v in invited_vendors:
                        col_v, col_p = st.columns([3, 2])
                        col_v.write(f"🏢 **{v.name}** ({v.email})")
                        price = col_p.number_input(f"Unit Price", min_value=0.0, step=0.1, key=f"p_{pr.id}_{v.id}")
                        if price > 0:
                            quote_entries.append({"vendor_id": v.id, "price": price, "name": v.name})
                    
                    st.markdown("---")
                    
                    if len(quote_entries) >= 1:
                        best_offer = min(quote_entries, key=lambda x: x['price'])
                        if len(quote_entries) == 1:
                            st.warning("ℹ️ Note: Only one quotation received (Sole Source).")
                        else:
                            st.info(f"💡 Recommended: **{best_offer['name']}** - **{best_offer['price']}**")
                        
                        if st.button(f"🏆 Confirm Award to {best_offer['name']}", key=f"aw_{pr.id}", type="primary"):
                            try:
                                for q in quote_entries:
                                    is_winner = (q['vendor_id'] == best_offer['vendor_id'])
                                    session.add(Quotation(pr_id=pr.id, vendor_id=q['vendor_id'], price=q['price'], is_awarded=is_winner))

                                pr.status = "Closed / Awarded"
                                session.commit()
                                # نوثق السعر الفائز والمورد، وأيضاً عدد المنافسين
                                log_system_action(
                                    user_email=os.getenv("SENDER_EMAIL", "Purchasing_Manager"),
                                    action="AWARD_CONTRACT",
                                    entity_type="Procurement",
                                    details=(
                                        f"Awarded PR #{pr.pr_number} to [{best_offer['name']}] "
                                        f"at Price: {best_offer['price']}. "
                                        f"Total bids compared: {len(quote_entries)}."
                                    )
                                )
                                st.balloons()
                                st.success(f"✅ Request {pr.pr_number} awarded.")
                                st.rerun()
                            except Exception as e:
                                session.rollback()
                                log_system_action(
                                    user_email=os.getenv("SENDER_EMAIL", "Purchasing_Manager"),
                                    action="AWARD_FAILURE",
                                    entity_type="Procurement",
                                    details=f"Failed to finalize awarding for PR #{pr.pr_number}. Error: {str(e)}",
                                    status="Failed"
                                )
                                st.error(f"❌ Error during awarding: {str(e)}")
                    else:
                        st.warning("⚠️ Waiting for at least 1 price entry.")