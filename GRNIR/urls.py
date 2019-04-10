from django.urls import path
from .views import *

urlpatterns = [
    path('supplier_po/list/',IntransitSupplierPOList,name='intransit-supplier-po-list'),
    path('supplier_po/<vpo_no>/lineitem/',IntransitSupplierPOLineitem,name='intransit-supplier-po-lineitem'),
]   