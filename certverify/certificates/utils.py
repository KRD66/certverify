# utils.py
from django.conf import settings
from django.urls import reverse
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape


def generate_qr_for_certificate(certificate):
    full_url = settings.SITE_DOMAIN + reverse("verify", args=[certificate.id])
    
    
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(full_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    filename = f"{certificate.id}.png"
    
    certificate.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
    


def generate_certificate_pdf(certificate):
    buffer = BytesIO()
    width, height = landscape(A4)
    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))

    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(width / 2, height - 100, "Certificate of Completion")

    pdf.setFont("Helvetica", 20)
    pdf.drawCentredString(width / 2, height - 160, certificate.recipient)

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(width / 2, height - 190, f"has completed {certificate.course}")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(60, 80, f"Issued: {certificate.issue_date.strftime('%d %b %Y')}")

    if certificate.expiry_date:
        pdf.drawString(60, 65, f"Expires: {certificate.expiry_date.strftime('%d %b %Y')}")
    else:
        pdf.drawString(60, 65, "Expires: Does not expire")

    pdf.drawString(60, 50, f"Certificate ID: {certificate.id}")

    if certificate.qr_code:
        pdf.drawImage(certificate.qr_code.path, width - 160, 40, width=100, height=100)

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
        