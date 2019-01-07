from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class NewClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimDetails
        fields = [
            'id',
            'employee',
            'claim_type',
            'description',
            'amount',
            'date',
            'document',
            'status',
            'created_at'
        ]
        read_only_fields = ('id','created_date','status')

class ClaimTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThirdClaimTypes
        fields = [
            'claim_type3'
        ]
        