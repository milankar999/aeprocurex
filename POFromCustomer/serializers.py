from rest_framework import serializers
from .models import *
from Employee.models import *
from django.contrib.auth.models import User

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
            'payment_terms',
        ]
        read_only_fields = (
            'id',
            'customer',
            'customer_contact_person',
            'delivery_contact_person',
            )

class CPOQuotationSelectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuotationTracker
        fields = [
            'quotation_no',
            'quotation_date',
            'rfp',
            'enquiry_reference',
        ]
        depth = 2

class CPOQuotationSelectionDoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = CPOSelectedQuotation
        fields = [
            'quotation_no',
            'CustomerPO'
        ]
        read_only_fields = (
            'CustomerPO',
        )

class CPOQuotationDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuotationLineitem
        fields = [
            'id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'part_number',
            'pack_size',
            'moq',
            'hsn_code',
            'gst',
            'quantity',
            'uom',
            'unit_price',
            'lead_time'
        ]
        
class CPOQuotationProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuotationLineitem
        fields = [
            'id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'part_number',
            'pack_size',
            'moq',
            'hsn_code',
            'gst',
            'quantity',
            'uom',
            'unit_price',
            'lead_time'
        ]

class CPOSelectedProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CPOLineitem
        fields = [
            'id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'part_no',
            'pack_size',
            'hsn_code',
            'gst',
            'quantity',
            'uom',
            'unit_price'
        ]

class CPOSelectedProductEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = CPOLineitem
        fields = [
            'id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'part_no',
            'pack_size',
            'hsn_code',
            'gst',
            'quantity',
            'uom',
            'unit_price'
        ]
        read_only_fields=('id',)

class CPOPendingApprovalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPO
        fields = [
            'id',
            'customer',
            'customer_contact_person',
            'customer_po_no',
            'customer_po_date',
        ]
        depth = 1

class CPOPendingApprovalLineitemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CPOLineitem
        fields = [
            'id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'part_no',
            'pack_size',
            'hsn_code',
            'gst',
            'quantity',
            'uom',
            'unit_price'
        ]
        read_only_fields=('id',)

class CPOApprovalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerPO
        fields = [
            'id',
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
        depth = 1

#Buyer List Serializer
class CPOBuyerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
        ]
        
#CPO Approve
class CPOApproveSerializer(serializers.ModelSerializer):

    class Meta:
        model = CPOAssign
        fields = [
            'assign_to',
        ]

class CPORejectedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPO
        fields = [
            'id',
            'customer',
            'customer_contact_person',
            'customer_po_no',
            'customer_po_date',
        ]
        depth = 1

class CPORejectedLineitemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CPOLineitem
        fields = [
            'id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'part_no',
            'pack_size',
            'hsn_code',
            'gst',
            'quantity',
            'uom',
            'unit_price'
        ]
        read_only_fields=('id',)

class CPORejectedProductEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = CPOLineitem
        fields = [
            'id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'part_no',
            'pack_size',
            'hsn_code',
            'gst',
            'quantity',
            'uom',
            'unit_price'
        ]
        read_only_fields=('id',)

class CPORejectedSupportingInfoEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPO
        fields = [
            'id',
            'customer_po_no',
            'customer_po_date',
            'delivery_date',
            'billing_address',
            'shipping_address',
            'inco_terms',
            'payment_terms',
        ]
        read_only_fields = (
            'id',
            )