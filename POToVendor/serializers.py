from rest_framework import serializers
from .models import *
from Employee.models import *
from POFromCustomer.models import *
from Supplier.models import *
from django.contrib.auth.models import User

#Pending CPO Selection
class PendingCPOListSerializer(serializers.ModelSerializer):
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

##Segmentation Serializer
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
            'unit_price',
            'discount',
        ]

#Vendor Product Segmentation API View
class PendingVPOVendorProductSegmentSerializer(serializers.ModelSerializer):
    vpo_lineitems = PendingVPOLineitemsSerializer(
        many=True,
        read_only=True)
    class Meta:
        model = VPO
        fields = [
            'id',
            'vendor',
            'vendor_contact_person',
            'offer_reference',
            'offer_date',
            'vpo_lineitems'
        ]
        depth = 1

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

#VPO Lineitem Edit
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
            'discount',
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

#VPO Basic Info Checking Serializer
class VPOBasicInfoCheckingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPO
        fields = [
            'id',
            'billing_address',
            'shipping_address',
            'delivery_date',
            'offer_reference',
            'offer_date',
            'payment_term',
            'advance_percentage',
            'freight_charges',
            'custom_duties',
            'pf',
            'insurance',
        ]
        read_only_fields = (
            'id',
        )

#VPO Supplier Contact Person Checking Serializer
class VPOSupplierCPInfoCheckingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPO
        fields = [
            'id',
            'vendor_contact_person'
        ]
        read_only_fields = (
            'id',
        )
        depth = 1

#VPO Supplier Contact Person Edit Operation
class VPOSCPEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierContactPerson
        fields = [
            'id',
            'name',
            'mobileNo1',
            'mobileNo2',
            'email1',
            'email2'
        ]
        read_only_fields = (
            'id',
        )

#VPO Supplier Info Checking Serializer
class VPOSupplierInfoCheckingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPO
        fields = [
            'id',
            'vendor'
        ]
        read_only_fields = (
            'id',
        )
        depth = 1

#VPO Update Info Vendor Serializer
class VPOUpdateVendorInfoSerializer(serializers.ModelSerializer):
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

#VPO receiver Serializer
class VPOReceiverSerilizer(serializers.ModelSerializer):
    class Meta:
        model = VPO
        fields = [
            'id',
            'receiver_name',
            'receiver_phone1',
            'receiver_phone2',
            'receiver_dept'
        ]
        read_only_fields = (
            'id',
        )

#VPO Terms and COnditions Serializer
class VPOTermsConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPO
        fields = [
            'id',
            'mode_of_transport',
            'inco_terms',
            'installation',
            'comments'
        ]
        read_only_fields = (
            'id',
        )

#VPO Delivery Instructions
class VPODISerializer(serializers.ModelSerializer):
    class Meta:
        model = VPO
        fields = [
            'id',
            'di1',
            'di2',
            'di3',
            'di4',
            'di5',
            'di6',
            'di7',
            'di8',
            'di9',
            'di10'
        ]
        read_only_fields = (
            'id',
        )

#Vendor PO Preview
class VPOPreviewSerializer(serializers.ModelSerializer):
    vpo_lineitems = PendingVPOLineitemsSerializer(
        many=True,
        read_only=True)
    class Meta:
        model = VPO
        fields = [
            'id',
            'vendor',
            'vendor_contact_person',
            'offer_reference',
            'offer_date',
            'billing_address',
            'shipping_address',
            'delivery_date',
            'requester',
            'receiver_name',
            'receiver_phone1',
            'receiver_phone2',
            'receiver_dept',
            'payment_term',
            'advance_percentage',
            'freight_charges',
            'custom_duties',
            'pf',
            'insurance',        
            'mode_of_transport',
            'inco_terms',
            'installation',
            'comments',
            'di1',
            'di2',
            'di3',
            'di4',
            'di5',
            'di6',
            'di7',
            'di8',
            'di9',
            'di10',
            'vpo_lineitems'
        ]


#VPO Preview Lineitems Serializer
class VPOPreviewLineitemsSerializer(serializers.ModelSerializer):
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
            'discount'
        ]      

#VPO Approval List
class VPOApprovalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPOTracker
        fields = [
            'po_number',
            'po_date',
            'vpo'
        ]
        depth = 1
        

#VPO Approval Lineitems Serializer
class VPOApprovalLineitemsSerializer(serializers.ModelSerializer):
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
            'discount'
        ]

#VPO Approval Info Serializer
class VPOApprovalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPO
        fields = [
            'vendor',
            'vendor_contact_person',
            'offer_reference',
            'offer_date',
            'billing_address',
            'shipping_address',
            'delivery_date',
            'requester',
            'receiver_name',
            'receiver_phone1',
            'receiver_phone2',
            'receiver_dept',
            'payment_term',
            'advance_percentage',
            'freight_charges',
            'custom_duties',
            'pf',
            'insurance',        
            'mode_of_transport',
            'inco_terms',
            'installation',
            'comments',
            'di1',
            'di2',
            'di3',
            'di4',
            'di5',
            'di6',
            'di7',
            'di8',
            'di9',
            'di10',
        ]
        depth = 1

#VPO Ready List
class VPOReadyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPOTracker
        fields = [
            'po_number',
            'po_date',
            'vpo'
        ]
        depth = 1

#Vendor PO  Ready Preview
class VPOReadyPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPOTracker
        fields = [
            'po_number',
            'po_date',
            'vpo'
        ]
        depth = 2