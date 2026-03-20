import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# تحميل البيانات من ملف .env
load_dotenv()

def send_rfq_email(to_email, subject, body, attachment_path):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    bcc_email = os.getenv("BCC_EMAIL")

    if not all([smtp_server, sender_email, sender_password]):
        return False, "إعدادات البريد غير مكتملة في ملف .env"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    rcpt_to = [to_email]
    if bcc_email:
        msg['Bcc'] = bcc_email
        rcpt_to.append(bcc_email)

    msg.attach(MIMEText(body, 'plain'))

    if os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(attachment_path)}")
            msg.attach(part)
    else:
        return False, "ملف الـ PDF لم يتم إنشاؤه بعد."

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg, sender_email, rcpt_to)
        server.quit()
        return True, "✅ تم إرسال الإيميل للمورد بنجاح مع نسخة للأرشفة!"
    except Exception as e:
        return False, f"❌ فشل الإرسال: {str(e)}"