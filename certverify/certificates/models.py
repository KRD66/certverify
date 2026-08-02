from django.db import models
import uuid 
from django.utils import timezone

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    recipient = models.CharField(max_length=100)
    issue_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(null=True,blank=True)
    is_revoked = models.BooleanField(default = False)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.CharField(max_length=150)
    
    
    @property
    def is_valid(self):
        if self.is_revoked:
            return False
        if self.expiry_date and self.expiry_date < timezone.now():
            return False
        return True
    
    
    def __str__(self):
        return f"{self.recipient} - {self.course} ({self.id})" 
            