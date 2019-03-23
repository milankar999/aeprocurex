from django.urls import path
from .views import *

urlpatterns = [
    path('customer_selection/',customer_selection,name='invoice-customer-selection'),
]   
