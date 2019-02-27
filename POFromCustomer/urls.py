from django.urls import path
from .views import *
from Quotation.models import *

urlpatterns = [
    path('create/customer_selection/',cpo_create_customer_selection,name='cpo-create-customer-selection'),
    path('create/<cust_id>/contact_person_selection/',cpo_create_contact_person_selection,name='cpo-create-contact-person-selection'),
    path('create/<cust_id>/<contact_person_id>/receiver_selection/',cpo_create_receiver_selection,name='cpo-create-receiver-selection'),
    path('create/<cust_id>/<contact_person_id>/<receiver_id>/quotation_selection/',cpo_create_quotation_selection,name='cpo-create-quotation-selection'),
    path('create/<quotation_no>/details/',cpo_quotation_details,name='cpo-quotation-details'),
    ]