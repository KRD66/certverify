from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.urls import reverse

import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor


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
    navy = HexColor("#1B3F8B")
    red = HexColor("#C1272D")
    ink = HexColor("#1A1A1A")

    pdf.setStrokeColor(navy)
    pdf.setLineWidth(2)
    pdf.rect(30, 30, width - 60, height - 60)

    pdf.setFillColor(red)
    pdf.rect(30, 30, 10, height - 60, fill=1, stroke=0)
    pdf.setFillColor(navy)
    pdf.rect(40, 30, 3, height - 60, fill=1, stroke=0)

    pdf.setFillColor(navy)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(70, height - 70, "CERTVERIFY")
    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(ink)
    pdf.drawString(70, height - 84, "Certificate Registry")

    pdf.setStrokeColor(navy)
    pdf.setLineWidth(1)
    pdf.rect(width - 230, height - 90, 190, 20, stroke=1, fill=0)
    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(ink)
    pdf.drawString(width - 222, height - 84, f"REF: {str(certificate.id)[:8].upper()}")

    pdf.setFillColor(ink)
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawCentredString(width / 2, height - 180, "Certificate of Completion")
    pdf.setFont("Helvetica", 18)
    pdf.drawCentredString(width / 2, height - 220, certificate.recipient)
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(width / 2, height - 245, f"has completed {certificate.course}")

    seal_x, seal_y = 110, 90
    pdf.setStrokeColor(red)
    pdf.setLineWidth(1.5)
    pdf.circle(seal_x, seal_y, 38, stroke=1, fill=0)
    pdf.setStrokeColor(navy)
    pdf.circle(seal_x, seal_y, 32, stroke=1, fill=0)
    pdf.setFillColor(navy)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawCentredString(seal_x, seal_y + 3, "VERIFIED")
    pdf.setFont("Helvetica", 6)
    pdf.drawCentredString(seal_x, seal_y - 7, "CERTVERIFY")

    pdf.setFillColor(ink)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(60, 65, f"Issued: {certificate.issue_date.strftime('%d %b %Y')}")
    expiry_text = certificate.expiry_date.strftime('%d %b %Y') if certificate.expiry_date else "Does not expire"
    pdf.drawString(60, 52, f"Expires: {expiry_text}")
    pdf.drawString(60, 39, f"Certificate ID: {certificate.id}")

    if certificate.qr_code:
        pdf.drawImage(certificate.qr_code.path, width - 160, 40, width=90, height=90)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.setFillColor(navy)
        pdf.drawCentredString(width - 115, 33, "Scan to verify")

    pdf.setFont("Helvetica", 7)
    pdf.setFillColor(HexColor("#555555"))
    verify_url = settings.SITE_DOMAIN + reverse("verify", args=[certificate.id])
    pdf.drawCentredString(width / 2, 20, f"Verify at {verify_url}")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer