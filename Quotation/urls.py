from django.urls import path
from .views import *

urlpatterns = [
    path('ready_to_generate/list/',generate_quotation_list,name='generate-quotation-list'),
    path('generate/<rfp_no>/lineitems/',generate_quotation_lineitem,name='generate-quotation-lineitem'),

    path('generate/<rfp_no>/lineitems/apply_other_charges/',generate_quotation_lineitem_apply_other_charges,name='generate-quotation-lineitem-apply-other-charges'),

    path('generate/<rfp_no>/lineitems/add_other_charges/',generate_quotation_lineitem_add_other_charges,name='generate-quotation-lineitem-add-other-charges'),
    path('generate/<rfp_no>/lineitems/<cost_id>/delete_cost/',generate_quotation_lineitem_cost_delete,name='generate-quotation-lineitem-cost-delete'),

    path('generate/<rfp_no>/lineitems/resourcing/',generate_quotation_resourcing,name='generate-quotation-lineitem-resourcing'),
    path('generate/<rfp_no>/lineitems/recoq/',generate_quotation_recoq,name='generate-quotation-lineitem-recoq'),
    path('generate/<rfp_no>/lineitems/<item_id>/edit/',generate_quotation_lineitem_edit,name='generate-quotation-lineitem-edit'),
    path('generate/<rfp_no>/lineitems/<item_id>/delete/',generate_quotation_lineitem_delete,name='generate-quotation-lineitem-delete'),
    path('generate/<rfp_no>/lineitems/<item_id>/price_fixing/',generate_quotation_price_fixing,name='generate-quotation-lineitem-price-fixing'),
    path('generate/<rfp_no>/lineitems/add/',generate_quotation_lineitem_add,name='generate-quotation-lineitem-add'),
    path('generate/<rfp_no>/lineitems/fill_margin/',generate_quotation_fill_margin,name='generate-quotation-fill-margin'),
    path('generate/<rfp_no>/lineitems/fill_leadtime/',generate_quotation_fill_leadtime,name='generate-quotation-fill-leadtime'),
    path('generate/<rfp_no>/lineitems/fill_brand/',generate_quotation_fill_brand,name='generate-quotation-fill-brand'),
    path('generate/<rfp_no>/lineitems/fill_moq/',generate_quotation_fill_moq,name='generate-quotation-fill-moq'),
    path('generate/<rfp_no>/lineitems/next_step/process/',generate_quotation_process,name='generate-quotation-process'),
    path('generate/<rfp_no>/lineitems/next_step/process/revised_existing/',generate_revised_existing,name='generate-revised-existing'),
    path('generate/<rfp_no>/lineitems/next_step/process/revised_new/',generate_revised_new,name='generate-revised-new'),
    path('generate/<rfp_no>/lineitems/next_step/process/<cust_id>/edit/',generate_quotation_edit_customer,name='generate-quotation-process-edit-customer'),
    path('generate/<rfp_no>/lineitems/next_step/process/<quotation_no>/column_selection/',generate_quotation_column_selection,name='generate-quotation-column-selection'),
    path('generate/<rfp_no>/lineitems/next_step/process/<quotation_no>/quotation_download/',download_quotation,name='download-quotation'),
    path('quoted/list/',quoted_list,name='quoted-list'),
    path('quoted/<rfp_no>/quotation_list/',quoted_quotation_list,name='quoted-quotation-list'),
    path('quoted/<rfp_no>/<quotation_no>/lineitems/',quotation_lineitems,name='quotation_lineitems'),
    path('quoted/<rfp_no>/<quotation_no>/lineitems/get_copy/',copy_quotation,name='copy_quotation'),
    path('quoted/<rfp_no>/<quotation_no>/lineitems/resourcing/',resourcing,name='resourcing'),
    path('quoted/<rfp_no>/<quotation_no>/lineitems/coq/',re_coq,name='re-coq'),
    path('quoted/<rfp_no>/<quotation_no>/lineitems/revised_quotation/',revised_quotation,name='revised-quotation'),
    path('immediate_quotation/selection/',immediate_quotation_selection,name='immediate-quotation-selection'),
    path('immediate_quotation/selection/<quotation_type>/customer_selection/',immediate_quotation_customer_selection,name='immediate-quotation-customer-selection'),
    path('immediate_quotation/selection/<quotation_type>/customer_selection/<cust_id>/contact_person_selection/',immediate_quotation_cperson_selection,name='immediate-quotation-customer-cperson-selection'),
    path('immediate_quotation/selection/<quotation_type>/customer_selection/<cust_id>/contact_person_selection/<contact_person_id>/enduser_selection/',immediate_quotation_enduser_selection,name='immediate-quotation-enduser-selection'),
    path('immediate_quotation/selection/<quotation_type>/customer_selection/<cust_id>/contact_person_selection/<contact_person_id>/enduser_selection/<enduser_id>/process/',immediate_quotation_process,name='immediate-quotation-processing'),
    path('immediate_quotation/product_selection/<rfp_no>/product_list/',immediate_quotation_product_selection,name='immediate-quotation-product-selection'),
]   