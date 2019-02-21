from django.urls import path,include
from rest_framework import routers
from .views import *

urlpatterns = [
    #CPO Creation
    path('customer_selection/',CustomerList.as_view()),
    path('customer/<customer_id>/contact_person_selection/',CustomerContactPersonView.as_view()),
    path('customer/<customer_id>/contact_person/<contact_person_id>/delivery_contactperson_selection/',DeliveryContactPersonView.as_view()),
    path('customer/<customer_id>/contact_person/<contact_person_id>/delivery_contactperson/<delivery_contact_person_id>/supporting_info/',SupportingInfoView.as_view()),
    path('customer/<customer_id>/contact_person/<contact_person_id>/delivery_contactperson/<delivery_contact_person_id>/store_supporting_info/',StoreSupportingInfoView.as_view()),
    path('customer/<cpo_id>/quotation_selection/',CPOQuotationSelectionView.as_view()),
    path('customer/<quotation_no>/quotation_details/',CPOQuotationDetailsView.as_view()),
    path('customer/<cpo_id>/quotation_selected/',CPOQuotationSelectedView.as_view()),
    path('customer/<cpo_id>/quotation_product_list/',CPOQuotationProductListView.as_view()),
    path('customer/<cpo_id>/quotation_product_selected/',CPOQuotationProductSelectedView.as_view()),
    path('customer/<cpo_id>/selected_product_list/',CPOSelectedProductListView.as_view()),
    path('customer/<cpo_id>/add_new_item/',CPOAddNewItemView.as_view()),
    path('customer/<cpo_id>/selected_product/<id>/edit/',CPOSelectedProductEditView.as_view()),
    path('customer/<cpo_id>/launch/',CPOlaunch.as_view()),

    #CPO Approval
    path('approval/approval_list/',CPOApprovalListView.as_view()),
    path('approval/<cpo_id>/lineitems/',CPOApprovalLineitemsView.as_view()),
    path('approval/<id>/informations/',CPOApprovalInfoView.as_view()),
    path('approval/buyer_list/',ByuerListView.as_view()),
    path('approval/<cpo_id>/approve/',CPOApprove.as_view()),
    path('approval/<cpo_id>/reject/',CPOReject.as_view()),

    #CPO Rectification
    path('rejected/rejected_list/',CPORejectedListView.as_view()),
    path('rejected/<cpo_id>/rejected_lineitems/',CPORejectedLineitemsView.as_view()),
    path('rejected/<cpo_id>/lineitem/<id>/edit/',CPORejectedProductEditView.as_view()),
    path('rejected/<id>/supporting_info_edit/',CPORejectedSupportingInfoEditView.as_view()),
    path('rejected/<id>/delete/',RejectedCPODelete.as_view()),
    path('rejected/<id>/mark_resolve/',RejectedCPOResolve.as_view()),
]