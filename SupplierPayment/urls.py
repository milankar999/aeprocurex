from django.urls import path
from SupplierPayment.views import *

urlpatterns = [
    path('make_new_request/po_selection/',VPOSelection,name='supplier-payment-request-po-selection'),
    path('make_new_request/<po_number>/request/',NewPaymentRequest,name='supplier-payment-request-create'),
    path('payment_request/applied_list/',SupplierPaymentAppliedList,name='supplier-payment-applied-list'),
    path('payment_request/<request_id>/delete/',SupplierPaymentRequestDelete,name='supplier-payment-request-delete'),
    path('payment_request/<request_id>/edit/',SupplierPaymentRequestEdit,name='supplier-payment-request-deit'),

    #Pending Approval
    path('payment_request/pending_approval_list_1/',SupplierPaymentPendingApprovalList1,name='supplier-payment-pending-approval-list-1'),
    path('payment_request/pending_approval_list_1/<request_id>/details/',SupplierPaymentPendingApprovalDetails1,name='supplier-payment-pending-approval-details-1'),
    path('payment_request/pending_approval_list_1/<request_id>/reject/',SupplierPaymentPendingApprovalReject1,name='supplier-payment-pending-approval-details-reject-1'),
    path('payment_request/pending_approval_list_1/<request_id>/approve/',SupplierPaymentPendingApprovalApprove1,name='supplier-payment-pending-approval-details-approve-1'),

    #Label1 Rejected List
    path('payment_request/lavel1/approved_list/',SupplierPaymentLabel1ApprovedList,name='supplier-payment-label-1-approved-list'),
    path('payment_request/lavel1/rejected_list/',SupplierPaymentLabel1RejectList,name='supplier-payment-label-1-rejected-list'),

    #View request_details
    path('payment_request/<request_id>/view_details/',SupplierPaymentViewRequestDetails,name='supplier-payment-view-request-details'),

    #Label 2 Pending Payment list
    path('payment_request/pending_payment_list/l2/',SupplierPaymentPendingPaymentList,name='supplier-payment-pending-payment-list-l2'),
    path('payment_request/pending_payment_list/l2/<request_id>/details/',SupplierPaymentPendingPaymentDetails,name='supplier-payment-pending-payment-details-l2'),

    #lavel2 reject
    path('payment_request/pending_approval_list_2/<request_id>/reject/',SupplierPaymentPendingApprovalReject2,name='supplier-payment-pending-approval-details-reject-2'),

    #Label2 Rejected List
    path('payment_request/lavel2/rejected_list/',SupplierPaymentLabel2RejectList,name='supplier-payment-label-2-rejected-list'),

    #Label2 add payment information
    path('payment_request/pending_approval_list_2/<request_id>/add_payment_information/',SupplierPaymentPendingAddPaymentInfo,name='supplier-payment-pending-add-payment-info'),

    #All Payment List
    path('all_payment_list/',SupplierPaymentAllList,name='supplier-payment-all-list'),

    #Wave
    path('payment_request/<id>/wave/',SupplierPaymentWave,name='supplier-payment-wave'),


    #-----------------Accounts------------------------------------
    path('accounts/all_payment_list/',AccountsSupplierPaymentList,name='accounts-supplier-payment-list'),
    path('accounts/payment/<id>/details/',AccountsPaymentDetails,name='accounts-payment-details'),
    path('accounts/payment/<id>/details/add_info/',AccountsPaymentDetailsAddInfo,name='accounts-payment-details-add-info'),
    path('accounts/payment/<id>/details/acknowledge/',AccountsPaymentDetailsAcknowledge,name='accounts-payment-details-acknowledge'),
    path('accounts/all_payment_list/acknowledge/list/',AccountsPaymentAcknowledgeList,name='accounts-payment-acknowledge-list'),
    path('accounts/all_payment_list/acknowledge/list/<id>/details/',AccountsPaymentAcknowledgeDetails,name='accounts-payment-acknowledge-details'),
]   



