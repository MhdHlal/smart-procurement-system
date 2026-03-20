import streamlit as st
import pandas as pd
from models.audit_log import AuditLog
# حذفنا استيراد SessionLocal لأنه لم يعد مطلوباً هنا

def show_audit_log_page(session): # أضفنا الـ session كمعامل للدالة
    st.title("🛡️ System Audit Trail")
    st.info("Log of all critical activities for transparency and oversight.")

    # نستخدم الـ session الممرر مباشرة بدل إنشائه
    try:
        all_logs = session.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
        
        if not all_logs:
            st.warning("No logs found in the system.")
            return

        # --- بقية الكود الخاص بك دون أي تغيير في المنطق أو التصميم ---
        log_data = [{
            "Timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "User": l.user_email,
            "Action": l.action,
            "Module": l.entity_type,
            "Details": l.details,
            "Status": "✅" if l.status == "Success" else "❌"
        } for l in all_logs]

        df = pd.DataFrame(log_data)

        col1, col2 = st.columns(2)
        with col1:
            search_user = st.text_input("🔍 Search by User")
        with col2:
            filter_action = st.multiselect("Filter Action", df["Action"].unique())

        if search_user:
            df = df[df["User"].str.contains(search_user, case=False)]
        if filter_action:
            df = df[df["Action"].isin(filter_action)]

        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Details": st.column_config.TextColumn("Activity Details", width="large"),
                "Timestamp": st.column_config.DatetimeColumn("Date & Time")
            }
        )
        
    except Exception as e:
        st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
    # حذفنا finally: session.close() لأن app.py هو المسؤول عن الإغلاق الآن