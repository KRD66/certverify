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
    gray = HexColor("#555555")

    margin = 40
    content_x = margin + 30

    pdf.setFillColor(red)
    pdf.rect(margin, margin, 8, height - 2 * margin, fill=1, stroke=0)
    pdf.setFillColor(navy)
    pdf.rect(margin + 8, margin, 3, height - 2 * margin, fill=1, stroke=0)

    top_y = height - margin - 30

    crest_cx, crest_cy = content_x + 18, top_y - 2
    pdf.setFillColor(navy)
    pdf.circle(crest_cx, crest_cy, 20, fill=1, stroke=0)
    pdf.setStrokeColor(red)
    pdf.setLineWidth(2)
    pdf.circle(crest_cx, crest_cy, 20, fill=0, stroke=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(crest_cx, crest_cy - 5, "CV")

    name_x = content_x + 50
    pdf.setFillColor(navy)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(name_x, top_y + 3, "CERTVERIFY CERTIFICATE")
    pdf.drawString(name_x, top_y - 13, "REGISTRY")
    pdf.setFont("Helvetica", 7.5)
    pdf.setFillColor(gray)
    pdf.drawString(name_x, top_y - 27, "Digitally issued and independently verifiable")

    box_w, box_h = 180, 17
    box_x = width - margin - 30 - box_w
    pdf.setStrokeColor(ink)
    pdf.setLineWidth(0.75)
    pdf.rect(box_x, height - margin - 30, box_w, box_h, stroke=1, fill=0)
    pdf.rect(box_x, height - margin - 51, box_w, box_h, stroke=1, fill=0)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.setFillColor(ink)
    pdf.drawString(box_x + 8, height - margin - 24, f"REF: {str(certificate.id)[:8].upper()}")
    pdf.drawString(box_x + 8, height - margin - 45, f"DATE: {certificate.issue_date.strftime('%d %b %Y').upper()}")

    addr_top = top_y - 65
    pdf.setFont("Helvetica-Bold", 12)
    pdf.setFillColor(ink)
    pdf.drawString(content_x, addr_top, certificate.recipient.upper())
    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(gray)
    line = addr_top - 13
    if certificate.matric_number:
        pdf.drawString(content_x, line, f"Matric No: {certificate.matric_number}")
        line -= 12
    pdf.drawString(content_x, line, "Certificate Registry — CertVerify")

    title_y = addr_top - 55
    pdf.setFont("Helvetica-Bold", 22)
    pdf.setFillColor(ink)
    pdf.drawString(content_x, title_y, "CERTIFICATE OF COMPLETION")
    pdf.setFillColor(red)
    pdf.rect(content_x, title_y - 12, 230, 3, fill=1, stroke=0)

    pdf.setFont("Helvetica", 10.5)
    pdf.setFillColor(ink)
    body_y = title_y - 40
    pdf.drawString(content_x, body_y, "This is to certify that the above-named recipient has fulfilled the")
    body_y -= 15
    pdf.drawString(content_x, body_y, "requirements for completion, and has been awarded this certificate")
    body_y -= 15
    pdf.drawString(content_x, body_y, "in")
    pdf.setFont("Helvetica-Bold", 10.5)
    course_text = certificate.course
    pdf.drawString(content_x + 14, body_y, course_text)
    text_width = pdf.stringWidth(course_text, "Helvetica-Bold", 10.5)
    pdf.setStrokeColor(ink)
    pdf.setLineWidth(0.5)
    pdf.line(content_x + 14, body_y - 3, content_x + 14 + max(text_width, 160), body_y - 3)
    body_y -= 15
    pdf.setFont("Helvetica", 10.5)
    pdf.drawString(content_x, body_y, "This certificate is issued as an authentic, independently verifiable record.")

    sig_y = margin + 130
    pdf.setStrokeColor(gray)
    pdf.setLineWidth(0.5)
    pdf.line(content_x, sig_y, content_x + 170, sig_y)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.setFillColor(ink)
    pdf.drawString(content_x, sig_y - 13, "Registrar, CertVerify")
    pdf.setFont("Helvetica", 8)
    pdf.setFillColor(gray)
    pdf.drawString(content_x, sig_y - 24, "For: Certificate Issuing Authority")

    seal_x, seal_y = content_x + 28, sig_y - 62
    pdf.setStrokeColor(red)
    pdf.setLineWidth(1.5)
    pdf.circle(seal_x, seal_y, 28, stroke=1, fill=0)
    pdf.setStrokeColor(navy)
    pdf.circle(seal_x, seal_y, 23, stroke=1, fill=0)
    pdf.setFillColor(navy)
    pdf.setFont("Helvetica-Bold", 7)
    pdf.drawCentredString(seal_x, seal_y + 2, "VERIFIED")
    pdf.setFont("Helvetica", 5)
    pdf.drawCentredString(seal_x, seal_y - 6, "CERTVERIFY")

    footer_y = margin + 30
    pdf.setFont("Helvetica", 8.5)
    pdf.setFillColor(ink)
    pdf.drawString(content_x, footer_y, f"Issued: {certificate.issue_date.strftime('%d %b %Y')}")
    expiry_text = certificate.expiry_date.strftime('%d %b %Y') if certificate.expiry_date else "Does not expire"
    pdf.drawString(content_x, footer_y - 12, f"Expires: {expiry_text}")
    pdf.drawString(content_x, footer_y - 24, f"Certificate ID: {certificate.id}")

    if certificate.qr_code:
        qr_size = 80
        qr_x = width - margin - 30 - qr_size
        qr_y = margin + 30
        pdf.drawImage(certificate.qr_code.path, qr_x, qr_y, width=qr_size, height=qr_size)
        pdf.setFont("Helvetica-Bold", 7.5)
        pdf.setFillColor(navy)
        pdf.drawCentredString(qr_x + qr_size / 2, qr_y - 11, "Scan to verify")

    bar_h = 20
    pdf.setFillColor(red)
    pdf.rect(margin, margin - bar_h - 6, width - 2 * margin, bar_h, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setFont("Helvetica-Bold", 7.5)
    verify_url = settings.SITE_DOMAIN + reverse("verify", args=[certificate.id])
    pdf.drawCentredString(width / 2, margin - bar_h + 3, f"Verify this certificate at {verify_url}")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer