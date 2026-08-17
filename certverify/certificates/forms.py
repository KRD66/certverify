from .models import Certificate
from django import forms 


class CertificateIssueForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['recipient', 'course','matric_number', 'issue_date', 'expiry_date', 'remarks']