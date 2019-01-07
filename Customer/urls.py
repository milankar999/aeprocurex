from django.urls import path
from Customer.views import *

urlpatterns = [
    path('',customers,name='customers'),
    path('<id>/details/',customer_details,name='customer_details'),
    path('<id>/edit/',customer_edit,name='customer_edit'),
    path('<id>/contact-person/',contact_person,name='contact_person'),
    path('<cust_id>/contact-person/<person_id>/edit/',contact_person_edit,name='contact_person_edit'),
    path('<id>/enduser/',enduser,name='enduser'),
    path('<cust_id>/enduser/<enduser_id>/edit/',enduser_edit,name='enduser_edit'),
    path('upload/customer_profile/',CustomerProfileUpload,name='customer-profile-upload')
]   
