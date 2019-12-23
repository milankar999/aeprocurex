from django.urls import path
from .views import *

urlpatterns = [
    path('',suppliers,name='supplier'),
    path('<id>/details/',supplier_details,name='supplier_details'),
    path('<id>/edit/',supplier_edit,name='supplier_edit'),

    #Document
    path('<id>/view_attachments/',supplier_documents,name='supplier_registration_documents'),
    path('<id>/view_attachments/<attachment_id>/delete/',supplier_documents_delete,name='supplier_registration_documents_delete'),

    path('<id>/contact-person/',supplier_contact_person,name='supplier_contact_person'),
    path('<supp_id>/contact-person/<person_id>/edit/',supplier_contact_person_edit,name='supplier_contact_person_edit'),
]   
