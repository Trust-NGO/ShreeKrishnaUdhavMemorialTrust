from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os
import qrcode


def generate_receipt_number(donation):

    year = datetime.now().year
    fin_year = f"{year}-{str(year + 1)[-2:]}"

    serial = str(donation.id).zfill(6)

    return f"SKUMT/{fin_year}/DEOS/{serial}"


def generate_receipt(donation, db):

    receipt_no = generate_receipt_number(donation)

    donation.receipt_no = receipt_no
    db.commit()

    file_name = f"receipt_{donation.id}.pdf"
    file_path = os.path.join("receipts", file_name)

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    elements = []

    # ================= HEADER =================
    header = Paragraph(
        "<b>SHRI KRISHNA UDHAV MEMORIAL TRUST</b><br/>"
        "Registered u/s 12A & Approved u/s 80G of Income Tax Act",
        styles["Title"]
    )
    elements.append(header)
    elements.append(Spacer(1, 10))

    # ================= 80G BLOCK =================
    tax = Paragraph(
        "<b>PAN:</b> AABTS1234C &nbsp;&nbsp; "
        "<b>80G Reg No:</b> SKT/80G/UP/2019/001<br/>"
        "<b>Donation Eligible for Tax Exemption under Section 80G</b>",
        styles["Normal"]
    )
    elements.append(tax)
    elements.append(Spacer(1, 15))

    # ================= RECEIPT DETAILS =================
    data = [
        ["Receipt No", receipt_no],
        ["Date", datetime.now().strftime("%d-%m-%Y")],
        ["Transaction ID", donation.transaction_id],
        ["Payment Status", donation.payment_status],
    ]

    table = Table(data, colWidths=[180, 300])
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f2f2f2")),
        ("PADDING", (0,0), (-1,-1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 15))

    # ================= DONOR DETAILS =================
    donor = [
        ["Name", donation.donor_name],
        ["Email", donation.donor_email],
        ["PAN (Optional for 80G)", donation.donor_pan or "N/A"],
        ["Amount", f"₹ {donation.amount}"],
        ["Purpose", donation.purpose],
    ]

    table2 = Table(donor, colWidths=[180, 300])
    table2.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("BACKGROUND", (0,0), (-1,0), colors.whitesmoke),
        ("PADDING", (0,0), (-1,-1), 8),
    ]))

    elements.append(table2)
    elements.append(Spacer(1, 20))

    # ================= QR VERIFICATION =================
    qr_data = f"""
    Receipt: {receipt_no}
    Name: {donation.donor_name}
    Amount: {donation.amount}
    PAN: {donation.donor_pan}
    """

    qr = qrcode.make(qr_data)
    qr_path = f"receipts/qr_{donation.id}.png"
    qr.save(qr_path)

    elements.append(Image(qr_path, width=100, height=100))
    elements.append(Spacer(1, 20))

    # ================= DECLARATION =================
    declaration = Paragraph(
        "This receipt is issued for donation received by Shri Krishna Udhav Memorial Trust.<br/>"
        "Eligible for deduction under Section 80G of Income Tax Act, subject to applicable rules.",
        styles["Normal"]
    )

    elements.append(declaration)
    elements.append(Spacer(1, 30))

    # ================= SIGNATURE =================
    sign = Paragraph(
        "<b>Authorized Signatory</b><br/>"
        "Finance Department<br/>Shri Krishna Udhav Memorial Trust",
        styles["Normal"]
    )

    elements.append(sign)

    # ================= WATERMARK =================
    def watermark(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 45)
        canvas.setFillColorRGB(0.92, 0.92, 0.92)
        canvas.rotate(45)
        canvas.drawCentredString(300, 0, "80G APPROVED DONATION")
        canvas.restoreState()

    doc.build(elements, onFirstPage=watermark)

    return receipt_no, f"/receipts/{file_name}"