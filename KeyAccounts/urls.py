from django.urls import path
from .views import *

urlpatterns = [
    path('enquiry_list/',enquiry_list,name='key_accounts_enquiry_list'),
    path('enquiry/<rfp_no>/lineitems/',enquiry_lineitems,name='key_accounts_enquiry_lineitems'),
    path('enquiry/<rfp_no>/lineitems/<lineitem_id>/edit/',enquiry_lineitems_edit,name='key_accounts_enquiry_lineitems_edit'),
]
