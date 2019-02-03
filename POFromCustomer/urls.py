from django.urls import path,include
from rest_framework import routers
from .views import *

urlpatterns = [
    path('customer_selection/',CustomerList.as_view()),
    path('customer/<customer_id>/contact_person_selection/',CustomerContactPersonView.as_view()),
    path('customer/<customer_id>/contact_person/<contact_person_id>/delivery_contactperson_selection/',DeliveryContactPersonView.as_view()),
    path('customer/<customer_id>/contact_person/<contact_person_id>/delivery_contactperson/<delivery_contact_person_id>/supporting_info/',SupportingInfoView.as_view()),
    path('customer/<customer_id>/contact_person/<contact_person_id>/delivery_contactperson/<delivery_contact_person_id>/store_supporting_info/',StoreSupportingInfoView.as_view()),
]