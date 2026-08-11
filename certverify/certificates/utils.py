# utils.py
from django.conf import settings
from django.urls import reverse
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


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
    