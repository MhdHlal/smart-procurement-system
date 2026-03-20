from database.config import SessionLocal
from models.audit_log import AuditLog
import logging

# إعداد السجل التقني الداخلي (كخطة بديلة لحفظ الأخطاء)
# تعديل بسيط لإضافة التوقيت في السجل النصي (system_errors.log)
logging.basicConfig(
    filename='system_errors.log', 
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s' # يضيف التاريخ والوقت لكل خطأ
)

def log_system_action(user_email: str, action: str, entity_type: str, details: str, status: str = "Success"):
    """
    خدمة مستقلة لتسجيل الحركات.
    تفتح وتغلق الجلسة الخاصة بها لضمان عدم تعطل التطبيق الرئيسي.
    """
    session = SessionLocal()
    try:
        new_log = AuditLog(
            user_email=user_email,
            action=action,
            entity_type=entity_type,
            details=details,
            status=status
        )
        session.add(new_log)
        session.commit()
    except Exception as e:
        logging.error(f"Failed to write to AuditLog: {str(e)}")
    finally:
        session.close()