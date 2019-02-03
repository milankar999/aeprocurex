from rest_framework import serializers
from .models import *

#Customer Selection
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'name',
            'location',
            'code',
            'city',
            'state',
        ]

#Customer Contact Person Selection
class CustomerContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContactPerson
        fields = [
            'id',
            'name',
            'mobileNo1',
            'mobileNo2',
            'email1',
            'email2',
            'customer_name',
        ]
        read_only_fields = ('id','customer_name')

#Delivery Contact Person Selection
class DeliveryContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryContactPerson
        fields = [
            'id',
            'person_name',
            'mobileNo1',
            'mobileNo2',
            'email1',
            'email2',
            'department_name',
        ]
        read_only_fields = ('id','customer_name')

class SupportingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = [
            'address',
            'billing_address',
            'shipping_address',
            'inco_term',
            'payment_term',
        ]
        read_only_fields = ('id','customer_name')

class StoreSupportingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPO
        fields = [
            'id',
            'customer',
            'customer_contact_person',
            'delivery_contact_person',
            'customer_po_no',
            'customer_po_date',
            'delivery_date',
            'billing_address',
            'shipping_address',
            'inco_terms',
            'payment_terms'
        ]
        