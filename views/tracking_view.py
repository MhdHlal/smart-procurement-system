import streamlit as st
import pandas as pd
from models.purchase_request import PurchaseRequest

def show_tracking_view(session):
    st.markdown("<h2 class='role-header'>📑 Order Tracking Dashboard</h2>", unsafe_allow_html=True)
    
    # جلب جميع الطلبات وترتيبها من الأحدث للأقدم
    all_prs = session.query(PurchaseRequest).order_by(PurchaseRequest.id.desc()).all()
    
    if not all_prs:
        st.info("ℹ️ No purchase requests found in the system yet.")
        return

    # 1. قسم الإحصائيات العلوية (KPIs) - أضفنا Archived هنا
    pending_count = sum(1 for pr in all_prs if pr.status == "Pending RFQ")
    sent_count = sum(1 for pr in all_prs if pr.status == "RFQ Sent")
    closed_count = sum(1 for pr in all_prs if pr.status == "Closed / Awarded")
    archived_count = sum(1 for pr in all_prs if pr.status == "Archived") # العداد الجديد

    c1, c2, c3, c4 = st.columns(4) # تغيير عدد الأعمدة إلى 4
    c1.metric("🔵 Pending", pending_count)
    c2.metric("🟡 Sent", sent_count)
    c3.metric("🟢 Awarded", closed_count)
    c4.metric("⚪ Archived", archived_count) # المقياس الجديد

    st.markdown("---")
    st.subheader("📋 Detailed Request Log")

    # 2. تجهيز البيانات للعرض
    data = []
    for pr in all_prs:
        # تحديد الأيقونة البصرية بناءً على الحالة (منطق محدث)
        if pr.status == "Pending RFQ":
            status_icon = "🔵"
        elif pr.status == "RFQ Sent":
            status_icon = "🟡"
        elif pr.status == "Closed / Awarded":
            status_icon = "🟢"
        elif pr.status == "Archived":
            status_icon = "⚪" # أيقونة رمادية/بيضاء للأرشفة
        else:
            status_icon = "❓"
        
        data.append({
            "PR Number": pr.pr_number,
            "Material": pr.material.material_name if pr.material else "N/A",
            "Quantity": pr.quantity,
            "Requested By": pr.requester_name,
            "Date": pr.requested_date,
            "Status": f"{status_icon} {pr.status}"
        })

    # العرض في جدول
    df = pd.DataFrame(data)
    st.dataframe(df, width='stretch', hide_index=True)