from django.urls import path
from .views import *

urlpatterns = [
    path('pending_enquiry_list/',pending_enquiry_list,name='reporting-pending-enquiry-list'),
    path('received_enquiry_list/',all_received_enquiry_list,name='reporting-all-received-enquiry-list'),
    path('enquiry/<rfp_no>/details/',enquiry_details,name='reporting-enquiry-details'),
    path('enquiry/<rfp_no>/sourcing_details/',enquiry_sourcing_details,name='reporting-enquiry-sourcing-details'),
    path('enquiry/<rfp_no>/quotation_details/',enquiry_quotation_details,name='reporting-enquiry-quotation-details'),

    path('generated_quotation_list/',generated_quotation_list,name='reporting-generated-quotation-list'),
    path('quotation/<quotation_no>/details/',generated_quotation_details,name='reporting-generated-quotation-details'),
    path('received_quotation_list/',received_quotation_list,name='reporting-received-quotation-list'),
    path('received_quotation/<sourcing_id>/details/',received_quotation_details,name='reporting-received-quotation-details'),

    #CPO Tracker
    path('pending_cpo_list/',pending_cpo_list,name='reporting-pending-cpo-list'),
    path('all_cpo_list/',all_cpo_list,name='reporting-all-cpo-list'),
    path('cpo/<cpo_id>/details/',cpo_details,name='reporting-cpo-details'),
    path('cpo/<cpo_id>/check_our_quotation/',cpo_quotation_reference,name='reporting-cpo-quotation-reference'),
    path('cpo/<cpo_id>/check_released_vpo_details/',cpo_vendorPO_details,name='reporting-cpo-vendorPO-details'),
    path('cpo/<cpo_id>/check_invoicing_details/',cpo_invoicing_details,name='reporting-cpo-invoicing-details'),

    #VPO Tracker
    path('open_vpo_list/',open_vpo_list,name='reporting-open-vpo-list'),
    path('all_vpo_list/',all_vpo_list,name='reporting-all-vpo-list'),
    path('vpo/<vpo_no>/details/',vpo_details,name='reporting-vpo-details'),

    ]