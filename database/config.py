import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. تحميل ملف .env (إذا وجد)
load_dotenv()

# 2. الحصول على رابط قاعدة البيانات من الـ .env مع وضع رابط "احتياطي" (Fallback) 
# لضمان عدم تعطل النظام إذا نسي المستخدم إعداد ملف الـ .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./procurement.db")

# 3. إعداد المحرك (Engine) مع مراعاة خصوصية SQLite
# ملاحظة: 'check_same_thread' مطلوبة فقط لـ SQLite، لذا نستخدم شرطاً بسيطاً
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # في حال انتقلت مستقبلاً لـ PostgreSQL أو MySQL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. إعداد الجلسة والقاعدة الأساسية (كما كانت تماماً لضمان التوافق)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 5. استدعاء إعدادات الإيميل لاستخدامها في ملفات الـ Logic
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))