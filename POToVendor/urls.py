from django.urls import path,include
from rest_framework import routers
from .views import *

urlpatterns = [
    #VPO Pending List
    path('pending_list/',PendingCPOList.as_view()),
    path('pending_cpo/<id>/lineitem_details/',PendingCPOLineitems.as_view()),
    path('pending_cpo/<id>/vendor_product_segmentation/',PendingCPOVendorProductSegmentation.as_view()),
    path('pending_cpo/<id>/unassigned_lineitem/',PendingCPOUnassignedLineitems.as_view()),
    path('pending_cpo/<cpo_id>/vpo/<vpo_id>/lineitem/<id>/edit/',VPOLineitemEdit.as_view()),

    #Steps for Un Assigned Products
    #VPO object Creation
    path('pending_cpo/<cpo_id>/new_vendor_selection/',VPONewVendorSelection.as_view()),
    path('pending_cpo/<cpo_id>/vendor/<id>/contact_person_selection/',VPONewVendorContactPersonSelection.as_view()),
    path('pending_cpo/<cpo_id>/vendor/<vendor_id>/contact_person/<contact_person_id>/create_vpo/',VPONewVenndorPOSegmentCreation.as_view()),
    
    #Add Lineitems to VPO
    path('pending_cpo/<cpo_id>/vpo/<vpo_id>/assign_lineitems/',VPOAssignProducts.as_view()),

    #VPO Supporting Info
    path('pending_cpo/<cpo_id>/vpo/<id>/basic_info_checking/',VPOBasicInfoChecking.as_view()),
    path('pending_cpo/<cpo_id>/vpo/<id>/supplier_contact_person_info_checking/',VPOSupplierCPInfoChecking.as_view()),
    
    #CURD Vendor Contact Person
    #path('pending_cpo/<cpo_id>/vpo/<vpo_id>/supplier_contact_person/',VPOSCPCURD.as_view()),
    path('pending_cpo/<cpo_id>/vpo/<vpo_id>/supplier_contact_person/<id>/edit/',VPOSCPEdit.as_view()),

    #Vendor Info Checking
    path('pending_cpo/<cpo_id>/vpo/<id>/supplier_info_checking/',VPOSupplierInfoChecking.as_view()),
    path('pending_cpo/<cpo_id>/vpo/<vpo_id>/supplier/<id>/update/',VPOSupplierInfoUpdate.as_view()),

    #Receiver Info
    path('pending_cpo/<cpo_id>/vpo/<id>/receiver_info/',VPOReceiverInfoChecking.as_view()),

    #Terms & Conditions
    path('pending_cpo/<cpo_id>/vpo/<id>/terms_conditions/',VPOTermsConditions.as_view()),

    #Delivery Instruction
    path('pending_cpo/<cpo_id>/vpo/<id>/delivery_instructions/',VPODeliveryInstructions.as_view()),

    #ASK for Approval
    path('pending_cpo/<cpo_id>/vpo/<vpo_id>/launch/',VPOLaunch.as_view()),

    #See The Demo Page
    path('pending_cpo/<cpo_id>/vpo/<id>/preview/',VPOPreview.as_view()),

    
]