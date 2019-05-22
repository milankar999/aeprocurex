from django.urls import path
from .views import *

urlpatterns = [

    #Received Via Vendor PO
    path('supplier_po/list/',IntransitSupplierPOList,name='intransit-supplier-po-list'),
    path('supplier_po/<vpo_no>/lineitem/',IntransitSupplierPOLineitem,name='intransit-supplier-po-lineitem'),
    path('supplier_po/<vpo_no>/proceed_for_grn/',SelectGRNLineitem,name='select-grn-lineitem'),
    path('supplier_po/<grn_no>/selected_lineitem/',GRNSelectedLineitem,name='grn-selected-lineitem'),
    path('supplier_po/<grn_no>/<item>/chnage_quantity/',GRNSelectedLineitemChangeQuantity,name='grn-selected-lineitem-change-quantity'),
    path('supplier_po/<grn_no>/<item>/remove/',GRNSelectedLineitemRemove,name='grn-selected-lineitem-remove'),
    
    path('supplier_po/<grn_no>/delete/',GRNDelete,name='grn-delete'),

    path('supplier_po/<grn_no>/grn_process_further/',GRNProcessFurther,name='grn-process-further'),

    path('supplier_po/<grn_no>/add_grn_document/',AddGRNDocument,name='add-grn-document'),
    path('supplier_po/<grn_no>/complete_grn/',CompleteGRN,name='complete-grn'),

    #Received Via Direct Processing Customer PO
    path('direct_processing_customer_po/list/',DirectProcessingCustomerPOList,name='direct-processing-customer-po-list'),
    path('direct_processing_customer_po/<cpo_no>/lineitem/',DirectProcessingCustomerPOLineitems,name='direct-processing-customer-po-lineitem'),
    path('direct_processing_customer_po/<cpo_no>/vendor_selection/',DirectProcessingCustomerPOVendorSelection,name='direct-processing-customer-po-vendor-selection'),
    path('direct_processing_customer_po/<cpo_no>/vendor/<vendor_id>/product_selection/',DirectProcessingCustomerPOProductSelection,name='direct-processing-customer-po-product-selection'),

    #Direct GRN
    path('direct_grn/vendor_selection/',DirectGRNVendorSelection,name='direct-grn-vendor-selection'),
    path('direct_grn/<grn_no>/product_entry/',DirectGRNProductEntry,name='direct-grn-product-entry'),
    path('direct_grn/<grn_no>/product_entry/<lineitem_id>/edit/',DirectGRNProductEdit,name='direct-grn-product-edit'),
    path('direct_grn/<grn_no>/product_entry/<lineitem_id>/delete/',DirectGRNProductDelete,name='direct-grn-product-delete'),



    ##--------------------Invoice Received-------------------------------
    path('invoice_received/pending_list/',IRPendingList,name='invoice-received-pending-list'),
    path('invoice_received/<grn_no>/details/',IRPendingGRNLineitem,name='invoice-received-pending-grn-lineitem'),
]   