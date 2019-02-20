from django.urls import path,include
from rest_framework import routers
from .views import *

urlpatterns = [
    #VPO Pending List
    path('pending_list/',PendingCPOList.as_view()),
    path('pending_cpo/<id>/lineitem_details/',PendingCPOLineitems.as_view()),
    path('pending_cpo/<id>/vendor_product_segmentation/',PendingCPOVendorProductSegmentation.as_view()),
    path('pending_cpo/<id>/vpo/<vpo_id>/details/',PendingCPOSegmentatedProduct.as_view()),
    path('pending_cpo/<id>/unassigned_lineitem/',PendingCPOUnassignedLineitems.as_view()),
    path('pending_cpo/<cpo_id>/vpo/<vpo_id>/lineitem/<id>/edit/',VPOLineitemEdit.as_view()),
    
    #Steps for Un Assigned Vendors
    path('pending_cpo/<cpo_id>/new_vendor_selection/',VPONewVendorSelection.as_view()),
    path('pending_cpo/<cpo_id>/vendor/<id>/contact_person_selection/',VPONewVendorContactPersonSelection.as_view()),
    path('pending_cpo/<cpo_id>/vendor/<vendor_id>/contact_person/<contact_person_id>/create_vpo/',VPONewVenndorPOSegmentCreation.as_view()),

    #
]