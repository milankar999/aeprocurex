from django.urls import path
from .views import *

urlpatterns = [
    path('pending_list/',rfp_pending_list,name='rfp-pending-list'),
    path('<rfp_no>/lineitems/',rfp_pending_lineitems,name='rfp_pending_lineitems'),
    path('<rfp_no>/lineitems/<lineitem_id>/edit-tax/',lineitem_edit_tax,name='lineitem-edit-tax'),
    path('<rfp_no>/lineitems/vendor_selection/',vendor_selection,name='vendor-selection'),
    path('<rfp_no>/lineitems/vendor_selection/single_price_request/',single_price_request,name='single-price-request'),
    path('<rfp_no>/lineitems/vendor_selection/new_vendor/',new_vendor,name='new-vendor'),
    path('<rfp_no>/lineitems/<vendor_id>/contact_person_selection/',vendor_contact_person_selection,name='vendor-contact-person-selection'),
    path('<rfp_no>/supplier/<vendor_id>/contact_person/<contact_person_id>/offer_reference/',offer_reference,name='offer_reference'),
    path('<rfp_no>/lineitems/vendor_quotation/<sourcing_id>/edit/',vendor_quotation_edit,name='vendor-quotation-edit'),
    path('<rfp_no>/lineitems/vendor_quotation/<sourcing_id>/delete/',vendor_quotation_delete,name='vendor-quotation-delete'),
    path('<rfp_no>/lineitems/vendor_quotation/<sourcing_id>/view/',vendor_quotation_view,name='vendor-quotation-view'),
    path('<rfp_no>/lineitems/vendor_quotation/<sourcing_id>/edit/<lineitem_id>/add/',vendor_quotation_price_add,name='vendor-quotation-price-add'),
    path('<rfp_no>/lineitems/vendor_quotation/<sourcing_id>/edit/<price_id>/edit/',vendor_quotation_price_edit,name='vendor-quotation-price-edit'),
    path('<rfp_no>/lineitems/vendor_quotation/<sourcing_id>/edit/<price_id>/delete/',vendor_quotation_price_delete,name='vendor-quotation-price-delete'),
    path('<rfp_no>/lineitems/vendor_quotation/<sourcing_id>/edit/<price_id>/round2/',round2,name='round2'),
    path('<rfp_no>/lineitems/vendor_selection/mark_as_completed/',sourcing_completed,name='sourcing-completed'),
    path('single_vendor/approval_list/pending/',single_vendor_approval_list,name='single-vendor-approval-list'),
    path('single_vendor/approval_list/pending/<rfp_no>/details/',single_vendor_approval_details,name='single-vendor-approval-details'),
    path('single_vendor/approval_list/pending/<rfp_no>/details/approve/',single_vendor_approve,name='single-vendor-approve'),
    path('single_vendor/approval_list/pending/<rfp_no>/details/reject/',single_vendor_reject,name='single-vendor-reject'),
    path('single_vendor/history/',single_vendor_history,name='single-vendor-history'),
    ]