from django.shortcuts import render, get_object_or_404, redirect
from .models import Certificate
from rest_framework import generics
from .serializer import CertificateSerializer
from django.urls import reverse
from django.http import HttpResponse
from .utils import generate_qr_for_certificate, generate_certificate_pdf
from django.contrib.auth.decorators import  staff_member_required, login_required
from .forms import CertificateIssueForm


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

@login_required
@staff_member_required
def issue_certificate_view(request):
    if request.method == "POST":
        form = CertificateIssueForm(request.POST)
        if form.is_valid():
            certificate = form.save
            return redirect("verify", cert_id=certificate.id)
    else:
        form = CertificateIssueForm()
            
    return render(request, "certificates/issue.html", {"form": form}) 





#FUNCTION issue_certificate_view(request):
    # this view must NOT be public — think about which Django decorator
    # restricts a view to logged-in staff users only. You've seen
    # `@login_required` conceptually — there's a similar one specifically
    # for staff/admin access.

    #if request.method == "POST":
        #form = CertificateIssueForm(request.POST)
        #if form.is_valid():
          #  save the form — this creates the Certificate, which triggers
          #  your existing save() override, which auto-generates the QR
         #   redirect somewhere useful (the verify page for the new cert?)
    #else:
     #   form = CertificateIssueForm()  # empty form for GET requests

    #render "certificates/issue.html" with the form in context
    
    #FUNCTION issue_certificate_view(request):
    #decorated with @staff_member_required

    #IF request.method == "POST":
     #   create form instance, filled with request.POST data
      #  IF form is valid:
       #     save the form — this returns the actual Certificate object
        #    that was just created (ModelForm.save() returns the instance)
         #   redirect to that certificate's verify page
        # if not valid, fall through — the form (now holding validation
        # errors) gets rendered again below, so the admin sees what
        # went wrong
   # ELSE:
    #    create an empty, unbound form instance (for the initial GET
     #   request showing a blank form)

    #render "certificates/issue.html" with the form in context