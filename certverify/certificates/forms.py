from .models import Certificate
from django import forms 


class CertificateIssueForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['recipient', 'course', 'issue_date', 'expiry_date', 'remarks']