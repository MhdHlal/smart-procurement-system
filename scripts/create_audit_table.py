from database.config import engine
from models.audit_log import AuditLog

print("⏳ Creating AuditLog table...")
AuditLog.metadata.create_all(bind=engine)
print("✅ AuditLog table created successfully!")