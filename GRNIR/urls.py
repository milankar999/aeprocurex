from django.urls import path
from .views import *

urlpatterns = [
    path('supplier_po/list/',IntransitSupplierPOList,name='intransit-supplier-po-list'),
    path('supplier_po/<vpo_no>/lineitem/',IntransitSupplierPOLineitem,name='intransit-supplier-po-lineitem'),
    path('supplier_po/<vpo_no>/proceed_for_grn/',SelectGRNLineitem,name='select-grn-lineitem'),
    path('supplier_po/<grn_no>/selected_lineitem/',GRNSelectedLineitem,name='grn-selected-lineitem'),
    path('supplier_po/<grn_no>/<item>/edit/',GRNSelectedLineitemEdit,name='grn-selected-lineitem-edit'),
  
]   