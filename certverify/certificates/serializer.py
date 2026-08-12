from .models import Certificate 
from rest_framework import serializers



class CertificateSerializer(serializers.ModelSerializer):
    is_valid = serializers.ReadOnlyField()
    
    class Meta:
        model = Certificate
        fields = [
    
            'id', 'recipient', 'course', 'issue_date', 'expiry_date',
            'is_revoked', 'remarks','qr_code', 'is_valid', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
                
                
class CertificatePublicSerializer(serializers.ModelSerializer):
    is_valid = serializers.ReadOnlyField()
    
    
    
    class Meta:
        model = Certificate
        fields = [' recipient', 'course', 'issue_date', 'expiry_date', 'is_valid']                