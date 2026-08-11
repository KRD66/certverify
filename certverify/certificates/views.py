from django.shortcuts import render, get_object_or_404
from .models import Certificate
from rest_framework import generics
from .serializer import CertificateSerializer
from django.urls import reverse


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
        

