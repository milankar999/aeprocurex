from django.urls import path,include
from rest_framework import routers
from .views import *

urlpatterns = [
    #VPO Pending List
    path('pending_list/',PendingCPOList.as_view()),
    path('pending_cpo/<id>/lineitem_details/',PendingCPOLineitems.as_view()),

    #Mark as Complet
    path('pending_cpo/<cpo_id>/mark_as_complet/',PendingCPOMarkCompleted.as_view()),

    path('pending_cpo/<id>/vendor_product_segmentation/',PendingCPOVendorProductSegmentation.as_view()),
    path('pending_cpo/<id>/unassigned_lineitem/',PendingCPOUnassignedLineitems.as_view()),
    path('pending_cpo/<cpo_id>/vpo/<vpo_id>/lineitem/<id>/edit/',VPOLineitemEdit.as_view()),

    #Remove VPO
    path('pending_cpo/<cpo_id>/vpo/<vpo_id>/remove_vpo/',VPORemove.as_view()),

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
    ##path('pending_cpo/<cpo_id>/vpo/<vpo_id>/supplier_contact_person/',VPOSCPCURD.as_view()),
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

    #Mark as 
    path('pending_cpo/<cpo_id>/vpo/<vpo_id>/request_direct_purchase/',VPOLaunchDirectPurchase.as_view()),

    #See The Demo Page
    path('pending_cpo/<cpo_id>/vpo/<vpo_id>/preview/',VPOPreview.as_view()),
    path('pending_cpo/<cpo_id>/vpo/<id>/preview_lineitems/',VPOPreviewLineitems.as_view()),

    #VPO Approval List
    #path('vpo/approval_list/',VPOApprovalList.as_view()),
    #path('vpo/<id>/<po_number>/lineitems/',VPOApprovalLineitems.as_view()),
    #path('vpo/<id>/<po_number>/info/',VPOApprovalInfo.as_view()),

    #path('vpo/<vpo_id>/<po_number>/preview/',VPOApprovalPreview.as_view()),    
    #path('vpo/<vpo_id>/<po_number>/lineitems/approve/',VPOApprove.as_view()),
    #path('vpo/<vpo_id>/<po_number>/lineitems/reject/',VPOReject.as_view()),

    
    #Application View
    #Regular VPO Approval list
    path('vendor_po/pending_approval_list/',VPOPendingApprovalList,name='vpo-pending-approval-list'),
    path('vendor_po/pending_approval/<po_number>/lineitems/',VPOPendingApprovalLineitems,name='vpo-pending-approval-lineitems'),
    path('vendor_po/pending_approval/<po_number>/get_copy/',VPOPendingApprovalGetCopy,name='vpo-pending-approval-get-copy'),
    path('vendor_po/pending_approval/<po_number>/approve/',VPOApprove,name='vpo-approve'),
    path('vendor_po/pending_approval/<po_number>/reject/',VPOReject,name='vpo-reject'),

    #Generating VPO
    path('vpo/ready_list/',VPOReadyList.as_view()),
    path('vpo/ready_list/<po_number>/details/',VPOReadyPreview.as_view()),
    path('vpo/ready_list/<po_number>/change_info/',VPOReadyChangeInfo.as_view()),

    path('vpo/ready_list/<po_number>/generate/po/',VPOGeneratePO.as_view()),

    #Generating VPO Directly
    path('approved_vendor_po/ready_list/',VPOApprovedReadyList,name='vpo-approved-ready-list'),
    path('approved_vendor_po/<po_number>/lineitems/',VPOApprovedReadyLineitems,name='vpo-approved-ready-lineitems'),
    path('approved_vendor_po/<po_number>/change_data/',VPOApprovedChangeData,name='vpo-approved-change-data'),
    path('approved_vendor_po/<po_number>/update_status/',VPOUpdateStatus,name='vpo-update-status'),

]