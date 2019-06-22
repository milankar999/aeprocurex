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

    path('vendor_po_prepare/pending_list/',VPOPreparePendingList,name='vpo-prepare-pending-list'),
    path('vendor_po_prepare/<cpo_id>/lineitems/',VPOPreparePendingLineitems,name='vpo-prepare-pending-lineitems'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/',VPOVendorProductSegmentation,name='vpo-vendor-product-segmentation'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/select_new_vendor/',VPOVendorProductSegmentationSelectNewVendor,name='vpo-vendor-product-segmentation-select-new-vendor'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/vendor/<vendor_id>/select_contact_person/',VPOVendorProductSegmentationSelectVendorContactPerson,name='vpo-vendor-product-segmentation-select-new-vendor-contact-person'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/vendor/<vendor_id>/contact_person/<contact_person_id>/confirmation/',VPOVendorProductSegmentationNewVendorConfirmation,name='vpo-vendor-product-segmentation-new-vendor-conformation'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_lineitem>/edit/',VPOVendorProductSegmentationLineitemEdit,name='vpo-vendor-product-segmentation-lineitem-edit'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_lineitem>/delete/',VPOVendorProductSegmentationLineitemDelete,name='vpo-vendor-product-segmentation-lineitem-delete'),

    #Assign a unselected lineitem
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_id>/assign_product/',VPOAssignProduct,name='vpo-vendor-product-segmentation-assign-product'),
    
    #Add Order Information
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_id>/add_order_info/',VPOAddOrderInformation,name='vpo-vendor-product-segmentation-add-order-information'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_id>/add_order_info/vendor_info_change/',VPOVendorInfoChange,name='vpo-vendor-info-change'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_id>/add_order_info/vendor_contact_person_edit/',VPOVendorContactPersonEdit,name='vpo-vendor-contact-person-edit'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_id>/add_other_expences/',VPOAddOtherExpences,name='vpo-add-other-expences'),

    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_id>/change_currency/',VPOChangeCurrency,name='vpo-change-currency'),

    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_id>/approval_request/',VPOApprovalRequest,name='vpo-approval-request'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_id>/mark_as_regular/',VPOMarkRegular,name='vpo-mark-as-regular-po'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_id>/mark_direct_buying/',VPOMarkDirectBuying,name='vpo-mark-as-regular-po'),
    path('vendor_po_prepare/<cpo_id>/vendor_product_segmentation/<vpo_id>/delete_vpo/',VPODelete,name='vpo-delete'),
    
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

    #path('approved_vendor_po/<po_number>/new_payment_request/',VPONewPaymentRequest,name='vpo-new-payment-request'),


    #Independent Vendor PO Creation
    path('vendor_po_prepare/independent_po_generation/creation_in_progress_list/',IVPOCreationInProgressList,name='indepen-vpo-creation-in-progress-list'),
    
    path('vendor_po_prepare/independent_po_generation/vendor_selection/',IVPOVendorSelection,name='indepen-vpo-vendor-selection'),
    path('vendor_po_prepare/independent_po_generation/vendor/<vendor_id>/contact_person_selection/',IVPOVendorContactPersonSelection,name='indepen-vpo-vendor-contact-person-selection'),
    path('vendor_po_prepare/independent_po_generation/vendor/<vendor_id>/contact_person/<contact_person_id>/confirmation/',IVPOConfirmation,name='indepen-vpo-confirmation'),

    path('vendor_po_prepare/independent_po_generation/<vpo_id>/product_selection/',IVPOProductSelection,name='indepen-vpo-product-selection'),

    path('vendor_po_prepare/independent_po_generation/<vpo_id>/product_selection/<item_id>/edit/',IVPOProductEdit,name='indepen-vpo-product-edit'),
    path('vendor_po_prepare/independent_po_generation/<vpo_id>/product_selection/<item_id>/delete/',IVPOProductdelete,name='indepen-vpo-product-delete'),

    path('vendor_po_prepare/independent_po_generation/<vpo_id>/add_order_info/',IVPOAddOrderInformation,name='indepen-vpo-add-order-info'),
    
    path('vendor_po_prepare/independent_po_generation/<vpo_id>/add_order_info/vendor_info_change/',IVPOVendorInfoChange,name='indepen-vpo-vendor-info-change'),
    path('vendor_po_prepare/independent_po_generation/<vpo_id>/add_order_info/vendor_contact_person_edit/',IVPOVendorContactPersonEdit,name='indepen-vpo-vendor-contact-person-edit'),
    path('vendor_po_prepare/independent_po_generation/<vpo_id>/add_other_expences/',IVPOAddOtherExpences,name='indepen-vpo-add-other-expences'),
    path('vendor_po_prepare/independent_po_generation/<vpo_id>/change_currency/',IVPOChangeCurrency,name='indepen-vpo-change-currency'),

    path('vendor_po_prepare/independent_po_generation/<vpo_id>/approval_request/',IVPOApprovalRequest,name='indepen-vpo-approval-request'),
    path('vendor_po_prepare/independent_po_generation/<vpo_id>/mark_as_regular/',IVPOMarkRegular,name='indepen-vpo-mark-as-regular-po'),
    path('vendor_po_prepare/independent_po_generation/<vpo_id>/mark_direct_buying/',IVPOMarkDirectBuying,name='indepen-vpo-mark-as-regular-po'),
    #path('vendor_po_prepare/independent_po_generation/<vpo_id>/delete_vpo/',IVPODelete,name='indepen-vpo-delete'),




    #add new payment terms
    path('<cpo_id>/<vpo_id>/add_new_vendor_payment_terms/', AddNewPaymentTerms, name='add-new-payment-terms'),
    path('<vpo_id>/add_new_vendor_payment_terms/', IAddNewPaymentTerms, name='independent-add-new-payment-terms'),
]