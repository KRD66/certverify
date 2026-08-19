from django.shortcuts import render, get_object_or_404, redirect
from .models import Certificate
from rest_framework import generics
from .serializer import CertificateSerializer
from django.urls import reverse
from django.http import HttpResponse
from .utils import generate_qr_for_certificate, generate_certificate_pdf
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CertificateIssueForm


def home_view(request):
    return render(request, "certificates/home.html")


@staff_member_required
def search_view(request):
    query = request.GET.get("q", "")

    if not query:
        return render(request, "certificates/search.html", {"results": []})
    results = Certificate.objects.filter(recipient__icontains=query)
    return render(request, "certificates/search.html", {"results": results})


def verify_view(request, cert_id):
    certificate = get_object_or_404(Certificate, id=cert_id)
    return render(request, "certificates/verify.html", {"certificate": certificate})


class CertificateListView(generics.ListCreateAPIView):
    queryset = Certificate.objects.all()
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


@staff_member_required
def issue_certificate_view(request):
    if request.method == "POST":
        form = CertificateIssueForm(request.POST)
        if form.is_valid():
            certificate = form.save()
            return redirect("verify", cert_id=certificate.id)
    else:
        form = CertificateIssueForm()

    return render(request, "certificates/issue.html", {"form": form})