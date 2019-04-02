from django.urls import path
from .views import *

urlpatterns = [
    path('intransit_customer_po_product/list/',IntransitCustomerPOList,name='intransit-customer-po-product-list'),
]   