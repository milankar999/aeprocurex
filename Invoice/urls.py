from django.urls import path
from .views import *

urlpatterns = [
    path('new_creation/purchase_order_selection/',purchare_order_selection,name='invoice-creation-purchase-order-selection'),
    path('new_creation/<cpo_id>/lineitem_selection/',invoice_lineitem_selection,name='invoice-lineitem-selection'),
    path('new_creation/<invoice_no>/selected_items/',invoice_selected_lineitem,name='invoice-selected-lineitem'),
    path('new_creation/<invoice_no>/delete/',invoice_delete,name='invoice-delete'),
    path('new_creation/<invoice_no>/selected_items/<lineitem_id>/edit/',invoice_selected_lineitem_edit,name='invoice-selected-lineitem-edit'),
    path('new_creation/<invoice_no>/selected_items/<lineitem_id>/delete/',invoice_selected_lineitem_delete,name='invoice-selected-lineitem-delete'),
    path('new_creation/<invoice_no>/continue/',invoice_continue,name='invoice-continue'),
    path('new_creation/<invoice_no>/generate_invoice/',invoice_generate,name='invoice-generate'),
    
    #Indirect Invoice // Invoice without vendor po
    path('new_creation/indirect/<invoice_no>/item_selection/',indirect_invoice_item_selection,name='indirect-invoice-item-selection'),
    path('new_creation/indirect/<invoice_no>/<cpo_lineitem_id>/select_item_from_inventory/',indirect_invoice_select_item_from_inventory,name='indirect-invoice-select-item-from-inventory'),
    path('new_creation/indirect/<invoice_no>/<cpo_lineitem_id>/<grn_lineitem_id>/select_item_from_inventory/choose_quantity/',indirect_invoice_inventory_choose_quantity,name='indirect-invoice-inventory-choose-quantity'),

    #Selected inventory item delete
    path('new_creation/indirect/<invoice_no>/item_selection/<link_id>/delete/',indirect_invoice_inventory_item_delete,name='indirect-invoice-inventory-item-delete'),
    
    #Continue to generate invoice
    path('new_creation/indirect/<invoice_no>/show_item_details/',indirect_invoice_show_item_details,name='indirect-invoice-show-item-details'),
    path('new_creation/indirect/<invoice_no>/continue/',indirect_invoice_continue,name='indirect-invoice-continue'),
    path('new_creation/indirect/<invoice_no>/generate_invoice/',indirect_invoice_generate,name='indirect-invoice-generate'),

    #indirect delete invoice
    path('new_creation/indirect/<invoice_no>/delete/',indirect_invoice_delete,name='indirect-invoice-delete'),

    #---DIRECT INVOICING
    path('new_creation/direct_invoice/customer_selection/',direct_invoice_customer_selection,name='direct-invoice-customer-selection'),
    path('new_creation/direct_invoice/customer/<customer_id>/contact_person_selection/',direct_invoice_customer_contact_person_selection,name='direct-invoice-customer-contact-person-selection'),
    path('new_creation/direct_invoice/customer/<customer_id>/contact_person/<contact_person_id>/receiver_selection/',direct_invoice_receiver_selection,name='direct-invoice-customer-contact-person-selection'),
    path('new_creation/direct_invoice/customer/<customer_id>/contact_person/<contact_person_id>/receiver/<delivery_contact_person_id>/invoice_number_generate/',direct_invoice_number_generate,name='direct-invoice-number-generate'),
    path('new_creation/direct_invoice/<invoice_no>/lineitem_selection/',direct_invoice_lineitem_selection,name='direct-invoice-lineitem-selection'),

    path('new_creation/direct_invoice/<invoice_no>/lineitem/<lineitem_id>/delete/',direct_invoice_lineitem_delete,name='direct-invoice-lineitem-delete'),
    path('new_creation/direct_invoice/<invoice_no>/lineitem/<lineitem_id>/edit/',direct_invoice_lineitem_edit,name='direct-invoice-lineitem-edit'),
    path('new_creation/direct_invoice/<invoice_no>/continue/',direct_invoice_continue,name='direct-invoice-continue'),
    path('new_creation/direct_invoice/<invoice_no>/generate_invoice/',direct_invoice_generate,name='direct-invoice-generate'),

    
    #Manage Invoices
    path('invoice_list/',invoice_list,name='invoice-list'),
    path('invoice_list/<invoice_no>/lineitems/',invoice_lineitems,name='invoice-lineitems'),



    #Invoice Acknowledgement
    path('pending_ack_list/',invoice_pending_ack_list,name='invoice-pending-ack-list'),
    path('pending_ack/<invoice_no>/details/',invoice_pending_ack_details,name='invoice-pending-ack-details'),
    path('pending_ack/<invoice_no>/acknowledge/',invoice_acknowledge,name='invoice-acknowledge'),

    path('ack_list/',invoice_ack_list,name='invoice-ack-list'),
    path('ack/<invoice_no>/details/',invoice_ack_details,name='invoice-ack-details'),
    path('ack/<invoice_no>/details/edit/',invoice_ack_edit,name='invoice-ack-edit'),

]   
