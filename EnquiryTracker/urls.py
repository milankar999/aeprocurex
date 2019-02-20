from django.urls import path
from .views import *

urlpatterns = [
    path('enquiry_list/',enquiry_list,name='enquiry_list'),
]   
