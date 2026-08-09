from django.shortcuts import render, get_object_or_404
from .models import Certificate


def home_view(request):
    return render (request, "certificates/home.html")


def search_view(request):
     query = request.GET.get("q", "") 
     
     if not query:
         return render(request, "certificates/search.html", {"results":[]})
     results  =  Certificate.objects.filter(recipient__icontains=query)
     return render(request, "certificates/search.html", {"results":results})



def verify_view(request,cert_id):
    certificate = get_object_or_404
    
    
    return render(request, "Certificates/verify.html", {"certificate": certificate})