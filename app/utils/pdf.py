import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

PDF_DIR = "generated_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

def generate_contract_pdf(order_id: int, buyer_name: str, seller_name: str, listing_title: str, amount: float) -> str:
    filename = f"contract_order_{order_id}.pdf"
    filepath = os.path.join(PDF_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2.0, height - 50, "Assignment of Real Estate Contract")

    # Body
    c.setFont("Helvetica", 12)
    text_lines = [
        f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}",
        "",
        f"Buyer: {buyer_name}",
        f"Seller: {seller_name}",
        "",
        f"Property: {listing_title}",
        f"Assignment Fee: ${amount:,.2f}",
        "",
        "This agreement confirms that the Seller has assigned the rights",
        "and interests in the above property to the Buyer upon payment.",
        "",
        "Signatures:",
        f"Buyer: ______________________",
        f"Seller: ______________________",
    ]

    y = height - 120
    for line in text_lines:
        c.drawString(72, y, line)
        y -= 20

    c.showPage()
    c.save()
    return filepath

