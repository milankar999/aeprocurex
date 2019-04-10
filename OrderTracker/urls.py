from django.urls import path
from .views import *

urlpatterns = [
    path('pending_customer_order_list/',pending_cpo_list,name='order-traker-pending_cpo_list'),
    path('pending_customer_order_list/<cpo_id>/details/',pending_cpo_lineitems,name='order-tracker-pending_cpo_lineitems'),
    path('pending_customer_order_list/<cpo_id>/change_quantity/',change_quantity_view,name='order-tracker-change-quantity'),
    path('pending_customer_order_list/<cpo_id>/change_quantity/<lineitem_id>/edit/',cpo_delivery_qty_update,name='order-tracker-delivery-qty-update'),

]   