from django.urls import path
from .views import *

urlpatterns = [
    path('',suppliers,name='supplier'),
    path('<id>/details/',supplier_details,name='supplier_details'),
    path('<id>/edit/',supplier_edit,name='supplier_edit'),
    path('<id>/contact-person/',supplier_contact_person,name='supplier_contact_person'),
    path('<supp_id>/contact-person/<person_id>/edit/',supplier_contact_person_edit,name='supplier_contact_person_edit'),
]   
