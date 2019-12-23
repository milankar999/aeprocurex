from django.urls import path
from .views import *

urlpatterns = [
    path('pending_customer_order_list/',pending_cpo_list,name='order-traker-pending_cpo_list'),
    path('pending_customer_order_list/<cpo_id>/details/',pending_cpo_lineitems,name='order-tracker-pending_cpo_lineitems'),
    path('pending_customer_order_list/<cpo_id>/details/reassign/',pending_cpo_reassign,name='order-tracker-pending_cpo_reassign'),
    path('pending_customer_order_list/<cpo_id>/change_quantity/',change_quantity_view,name='order-tracker-change-quantity'),
    path('pending_customer_order_list/<cpo_id>/change_quantity/<lineitem_id>/edit/',cpo_delivery_qty_update,name='order-tracker-delivery-qty-update'),

    #view Supplier Purchase order
    path('pending_customer_order_list/<cpo_id>/view_supplier_purchase_order/',cpo_to_vew_supplier_order,name='order-tracker-view-supplier-order'),
    
    #Edit Customer PO by CRM
    path('pending_customer_order_list/<cpo_id>/change_orderdetails/',change_order_details,name='order-tracker-change-order-details'),
    path('pending_customer_order_list/<cpo_id>/add_new_lineitem/',change_order_add_new_item,name='change-order-add-new-item'),
    path('pending_customer_order_list/<cpo_id>/<lineitem_id>/edit/',change_order_lineitem_edit,name='change-order-lineitem-edit'),
    path('pending_customer_order_list/<cpo_id>/change_customer/customer_selection/',change_order_customer_selection,name='change-order-customer-selection'),
    path('pending_customer_order_list/<cpo_id>/change_customer/<customer_id>/confirmation/',change_order_change_customer,name='change-order-change-customer'),
    path('pending_customer_order_list/<cpo_id>/change_contact_person/contact_person_selection/',change_order_contact_person_selection,name='change-order-contact-person-selection'),
    path('pending_customer_order_list/<cpo_id>/change_contact_person/<contact_person_id>/confirmation/',change_order_change_contact_person,name='change-order-change-contact-person'),

]   