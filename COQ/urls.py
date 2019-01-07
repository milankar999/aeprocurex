from django.urls import path
from .views import *

urlpatterns = [
    path('pending_list/',coq_pending_list,name='coq_pending_list'),
    path('pending_list/<rfp_no>/details/',coq_pending_details,name='coq_pending_details'),
    path('pending_list/<rfp_no>/details/<sourcing_id>/select/',coq_price_select,name='coq_price_select'),
    path('pending_list/<rfp_no>/details/auto_coq/',auto_coq,name='auto-coq'),
    path('pending_list/<rfp_no>/details/reset_coq/',reset_coq,name='reset-coq'),
]   
