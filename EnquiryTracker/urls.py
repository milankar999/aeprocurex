from django.urls import path
from .views import *

urlpatterns = [
    path('enquiry_list/',enquiry_list,name='enquiry_list'),
    path('lineitem_list/',lineitem_list,name='enquiry_lineitem_list'),
    path('rfp/<rfp_no>/lineitems/',rfp_lineitem,name='tracker_rfp_lineitem'),
]   