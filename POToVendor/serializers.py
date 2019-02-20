from rest_framework import serializers
from .models import *
from Employee.models import *
from POFromCustomer.models import *
from Supplier.models import *
from django.contrib.auth.models import User

#Pending CPO Selection
class PendingVPOListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPO
        fields = [
            'id',
            'customer',
            'customer_contact_person',
            'customer_po_no',
            'delivery_date',
        ]
        depth = 1
        
#Pending CPO Lineitems
class PendingCPOLineitemsSerializer(serializers.ModelSerializer):
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
            'hsn_code',
            'pack_size',
            'gst',
            'uom',
            'quantity',
        ]

#Vendor Product Segmentation API View
class PendingVPOVendorProductSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPO
        fields = [
            'id',
            'vendor',
            'vendor_contact_person',
            'offer_reference',
            'offer_date',
        ]
        depth = 1

#Segmented Product Lineitems
class PendingVPOLineitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPOLineitems
        fields = [
            'id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'hsn_code',
            'pack_size',
            'gst',
            'uom',
            'quantity',
        ]

#Unassigned Product Lineitems
class PendingCPOUnassignedLineitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPOLineitems
        fields = [
            'id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'hsn_code',
            'pack_size',
            'gst',
            'uom',
            'quantity',
        ]

#VPO Product Edit
class PendingVPOLineitemEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPOLineitems
        fields = [
            'id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'hsn_code',
            'pack_size',
            'gst',
            'uom',
            'quantity',
            'unit_price',
        ]

        read_only_fields = (
            'id',
        )

#VPO New Vendor Serializer
class VPONewVendorSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierProfile
        fields = [
            'id',
            'name',
            'location',
            'address',
            'city',
            'state',
            'pin',
            'country',
            'office_email1',
            'office_email2',
            'office_phone1',
            'office_phone2',
            'gst_number',
            'payment_term',
            'advance_persentage',
            'inco_term'
        ]
        read_only_fields = (
            'id',
        )

#VPO Vendor Contact Person Serializer
class VPOVendorCOntactPersonSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierContactPerson
        fields = [
            'id',
            'name',
            'mobileNo1',
            'mobileNo2',
            'email1',
            'email2',
            'supplier_name'
        ]
        read_only_fields = (
            'id',
            'supplier_name'
        )

#VPO New Segment Create
class VPONewVenndorPOSegmentCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPO
        fields = [
            'cpo',
            'vendor',
            'vendor_contact_person',
            'billing_address',
            'shipping_address',
            'requester',
            'payment_term',
            'advance_percentage',
            'currency',
            'di1',
            'di2',
            'di3',
            'di4',
            'di5'
        ]
        read_only_fields = (
            'cpo',
            'vendor',
            'vendor_contact_person',
            'billing_address',
            'shipping_address',
            'requester',
            'payment_term',
            'advance_percentage',
            'currency',
            'di1',
            'di2',
            'di3',
            'di4',
            'di5'
        )