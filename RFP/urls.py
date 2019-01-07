from django.urls import path
from RFP.views import *

urlpatterns = [
    path('create/',rfp_create,name='rfp-create'),
    path('create/<cust_id>/',contact_person,name='contact-person-selection'),
    path('create/<cust_id>/<contactperson_id>/',end_user,name='enduser-selection'),
    path('create/<cust_id>/<contactperson_id>/<enduser_id>/',processing,name='processings'),
    path('in_progress/list/',rfp_creation_inprogress,name='rfp-creation-progress'),
    path('create/product_selection/1/2/3/<rfp_no>/',product_selection,name='product-selection'),
    path('create/product_selection/1/2/3/<rfp_no>/<lineitem_id>/',lineitem_edit,name='lineitem-edit'),
    path('create/product_selection/1/2/3/<rfp_no>/<lineitem_id>/delete/',lineitem_delete,name='lineitem-delete'),
    path('<rfp_no>/generate/',rfp_generate,name='rfp_generate'),
    path('approval/list/',rfp_approval_list,name='rfp-approval-list'),
    path('approval/<rfp_no>/lineitems/',rfp_approval_lineitems,name='rfp-approval-lineitems'),
    path('<rfp_no>/reject/',rfp_reject,name='rfp-reject'),
    path('<rfp_no>/approve/',rfp_approve,name='rfp-approve'),
    path('rejected/list/',rfp_rejected_list,name='rfp-rejected_list'),
    ]