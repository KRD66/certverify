from django.urls import path 
from . import views
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [
    path("", views.home_view, name="home"),
    path("search/", views.search_view, name= "search"),
    path("verify/<uuid:cert_id>/", views.verify_view, name="verify"),
    path("api/certificates/",views.CertificateListView.as_view(),name="certificate-list"),
    path("api/certificates/<uuid:pk>/", views.CertificateDetailView.as_view(), name="certificate-detail"),
    path("download/<uuid:cert_id>/", views.download_certificate_pdf, name="download"),
    path("issue/", views.issue_certificate_view, name="issue"),
    path('login/', LoginView.as_view(template_name='certificates/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]