from django.urls import path
from .views import *
from Quotation.models import *

urlpatterns = [
    path('create/customer_selection/',cpo_create_customer_selection,name='cpo-create-customer-selection'),
    path('create/<cust_id>/contact_person_selection/',cpo_create_contact_person_selection,name='cpo-create-contact-person-selection'),
    path('create/<cust_id>/<contact_person_id>/receiver_selection/',cpo_create_receiver_selection,name='cpo-create-receiver-selection'),
    path('create/<cust_id>/<contact_person_id>/<receiver_id>/process/',cpo_process,name='cpo-process'),
    path('create/<cpo_id>/quotation_selection/',cpo_create_quotation_selection,name='cpo-create-quotation-selection'),
    path('create/<cpo_id>/quotation_selection_skip/',cpo_create_quotation_selection_skip,name='cpo-create-quotation-selection-skip'),
    path('quotation_no_search/',cpo_quotation_no_search,name='cpo-quotation-no-search'),
    path('create/<quotation_no>/details/',cpo_quotation_details,name='cpo-quotation-details'),

    path('create/<cpo_id>/quotation_lineitem_selection/',cpo_create_quotation_lineitem_selection,name='cpo-create-quotation-lineitem-selection'),
    path('create/<cpo_id>/selected_lineitems/',cpo_create_selected_lineitem,name='cpo-create-selected-lineitem'),
    path('create/<cpo_id>/selected_lineitems/<lineitem_id>/edit/',cpo_create_lineitem_edit,name='cpo-create-ineitem-edit'),
    path('create/<cpo_id>/selected_lineitems/<lineitem_id>/delete/',cpo_create_lineitem_delete,name='cpo-create-ineitem-delete'),
    path('create/<cpo_id>/selected_lineitems/generate/',cpo_generate,name='cpo-generate'),

    path('creation_in_progress/list/',cpo_creation_inprogress_list,name='cpo-creation-in-progress'),
    path('creation_in_progress/<cpo_id>/details/',cpo_creation_inprogress_details,name='cpo-creation-in-progress-details'),

    #Approval List
    path('cpo_approval/list/',cpo_approval_list,name='cpo-approval-list'),
    path('cpo_approval/<cpo_id>/lineitem/',cpo_approval_lineitem,name='cpo-approval-lineitem'),
    path('cpo_approval/<cpo_id>/lineitem/check_quotation_reference/',cpo_approval_quotation_reference,name='cpo-approval-quotation-reference'),
    path('cpo_approval/<cpo_id>/reject/',cpo_reject,name='cpo-reject'),
    path('cpo_approval/<cpo_id>/approve/',cpo_approve,name='cpo-approve'),

    path('cpo_approval/<cpo_id>/mark_as_direct_vendor_order_processing/',mark_direct_processing,name='cpo-mark-direct-processing'),

    path('cpo/rejected_list/',cpo_rejected_list,name='cpo-rejected-list'),
    path('rejected_cpo/<cpo_id>/lineitems/',cpo_rejected_lineitem,name='cpo-rejected-lineitems'),
]