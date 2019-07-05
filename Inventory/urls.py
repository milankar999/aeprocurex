from django.urls import path
from .views import *

urlpatterns = [

    #Accounts
    path('all_inventory/grn/',InventoryByGRN,name='inventory-by-grn'),
]   