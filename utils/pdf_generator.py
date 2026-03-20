from fpdf import FPDF
import sqlite3

def get_settings():
    conn = sqlite3.connect('procurement.db')
    cur = conn.cursor()
    cur.execute("SELECT company_name, company_email, company_web, payment_terms, delivery_terms, currency FROM system_settings LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row if row else ("Averroa Division", "info@averroa.com", "www.averroa.com", "N/A", "N/A", "USD")

def generate_rfq_pdf(rfq, file_path):
    settings = get_settings()
    pdf = FPDF()
    pdf.add_page()
    
    # Header & Company Info from DB
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "REQUEST FOR QUOTATION (RFQ)", ln=True, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 7, settings[0], ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, f"Email: {settings[1]} | Web: {settings[2]}", ln=True, align='C')
    pdf.ln(10)
    
    # Data Mapping
    req_name = getattr(rfq.pr, 'requester_name', None) or "Procurement Dept"
    req_date = getattr(rfq.pr, 'requested_date', None) or "N/A"
    mat_name = rfq.pr.material.material_name if rfq.pr.material else "N/A"
    mat_unit = rfq.pr.material.unit if rfq.pr.material else "N/A"
    
    # References Table
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 8, "RFQ Number:", border=1, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(50, 8, str(rfq.rfq_number), border=1)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 8, "PR Reference:", border=1, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(60, 8, str(rfq.pr.pr_number), border=1, ln=True)
    
    # Dates
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 8, "Requested Date:", border=1, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(50, 8, str(req_date), border=1)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 8, "Quotation Due:", border=1, fill=True)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(60, 8, rfq.deadline.strftime("%Y-%m-%d"), border=1, ln=True)
    pdf.set_text_color(0, 0, 0)

    # Requester
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 8, "Contact Person:", border=1, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(150, 8, f"{req_name} (Procurement Specialist)", border=1, ln=True)
    pdf.ln(8)

    # Material Table
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Material Specifications & Quantities:", ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(80, 10, "Description", border=1, align='C', fill=True)
    pdf.cell(40, 10, "Quantity", border=1, align='C', fill=True)
    pdf.cell(30, 10, "Unit", border=1, align='C', fill=True)
    pdf.cell(40, 10, "Currency", border=1, align='C', fill=True, ln=True)
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(80, 10, mat_name, border=1, align='C')
    pdf.cell(40, 10, str(rfq.pr.quantity), border=1, align='C')
    pdf.cell(30, 10, mat_unit, border=1, align='C')
    pdf.cell(40, 10, settings[5], border=1, align='C', ln=True)
    pdf.ln(8)
    
    # Terms & Conditions from DB
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Terms and Conditions:", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.cell(0, 6, f"- Payment Terms: {settings[3]}", ln=True)
    pdf.cell(0, 6, f"- Delivery Terms: {settings[4]}", ln=True)
    pdf.cell(0, 6, "- Quotations must be valid for at least 30 days.", ln=True)
    pdf.cell(0, 6, "- Quality: Must meet international standards.", ln=True)
    pdf.ln(5)

    # Instructions
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "Special Instructions:", ln=True)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 8, str(rfq.vendor_instructions), border=1)
    
    pdf.output(file_path)
