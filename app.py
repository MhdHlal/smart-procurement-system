import streamlit as st
import os
from datetime import datetime
from database.config import SessionLocal, engine, Base

# استيراد الموديلات
from models import RawMaterial, Product, BOM
from models.purchase_request import PurchaseRequest
from models.rfq import RFQ
from models.vendor import Vendor
from models.quotation import Quotation

# استيراد الواجهات
from views.planning_view import show_planning_view
from views.purchasing_view import show_purchasing_view
from views.admin_view import show_admin_view
from views.tracking_view import show_tracking_view
from views.audit_view import show_audit_log_page

# تحديث هيكلية قاعدة البيانات تلقائياً
Base.metadata.create_all(bind=engine)

st.set_page_config(page_title="Averroa ERP - Digital Transformation MVP", layout="wide")

# ARCHIVE SETUP
ARCHIVE_DIR = os.path.join("rfq_archive", datetime.now().strftime("%Y"), datetime.now().strftime("%m"))
if not os.path.exists(ARCHIVE_DIR): os.makedirs(ARCHIVE_DIR)

# STYLING
st.markdown("""
    <style>
    div.stButton > button:contains("🗑️") { background-color: #ff4b4b !important; color: white !important; }
    div.stButton > button:contains("💾") { background-color: #28a745 !important; color: white !important; }
    .role-header { color: #1E3A8A; font-weight: bold; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- نظام الصلاحيات والأدوار (النسخة الاحترافية المُحدثة) ---
st.sidebar.title("👤 Role-Based Access")
# أضفنا دور "إدارة المصنع"
user_role = st.sidebar.radio("Identify Your Department:", ["Planning Team", "Purchasing Team", "Factory Management"])
st.sidebar.markdown("---")

# توجيه القوائم بناءً على الدور (فصل المهام الصارم)
if user_role == "Planning Team":
    choice = st.sidebar.selectbox("Navigation", ["Create Purchase Request"])
elif user_role == "Purchasing Team":
    choice = st.sidebar.selectbox("Navigation", ["Manage RFQs & Quotations"])
else: # Factory Management
    choice = st.sidebar.selectbox("Navigation", ["Order Tracking Dashboard", "Admin: Master Data", "System Audit Logs"])

# إدارة الجلسة (Session Handling)
session = SessionLocal()

try:
    # ROUTING LOGIC (تنفيذ التوجيه)
    if choice == "Create Purchase Request":
        show_planning_view(session)
    elif choice == "Manage RFQs & Quotations":
        show_purchasing_view(session, ARCHIVE_DIR)
    elif choice == "Order Tracking Dashboard":
        show_tracking_view(session)
    elif choice == "Admin: Master Data":
        show_admin_view(session)
    elif choice == "System Audit Logs": 
        show_audit_log_page(session)
finally:
    session.close()