from django.urls import path
from .views import *

urlpatterns = [
    path('new_creation/purchase_order_selection/',purchare_order_selection,name='invoice-creation-purchase-order-selection'),
    path('new_creation/<cpo_id>/lineitem_selection/',invoice_lineitem_selection,name='invoice-lineitem-selection'),
    path('new_creation/<invoice_no>/selected_items/',invoice_selected_lineitem,name='invoice-selected-lineitem'),
    path('new_creation/<invoice_no>/selected_items/<lineitem_id>/edit/',invoice_selected_lineitem_edit,name='invoice-selected-lineitem-edit'),
    path('new_creation/<invoice_no>/selected_items/<lineitem_id>/delete/',invoice_selected_lineitem_delete,name='invoice-selected-lineitem-delete'),
    path('new_creation/customer_selection/',customer_selection,name='invoice-customer-selection'),
]   
