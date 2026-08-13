from django.shortcuts import render, get_object_or_404
from .models import Certificate
from rest_framework import generics
from .serializer import CertificateSerializer
from django.urls import reverse
from django.http import HttpResponse
from .utils import generate_qr_for_certificate, generate_certificate_pdf


def home_view(request):
    return render (request, "certificates/home.html")


def search_view(request):
     query = request.GET.get("q", "") 
     
     if not query:
         return render(request, "certificates/search.html", {"results":[]})
     results  =  Certificate.objects.filter(recipient__icontains=query)
     return render(request, "certificates/search.html", {"results":results})



def verify_view(request,cert_id):
    certificate = get_object_or_404(Certificate, id=cert_id)
    
    return render(request, "certificates/verify.html", {"certificate": certificate})

class CertificateListView(generics.ListCreateAPIView):
    queryset =  Certificate.objects.all()
    serializer_class = CertificateSerializer
    
 
class CertificateDetailView(generics.RetrieveUpdateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    
    
        

def download_certificate_pdf(request, cert_id):
    certificate = get_object_or_404(Certificate, id=cert_id)
    buffer = generate_certificate_pdf(certificate)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate-{certificate.id}.pdf"'
    return response