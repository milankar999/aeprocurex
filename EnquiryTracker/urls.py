from django.urls import path
from .views import *

urlpatterns = [
    path('pending_enquiry_list/',pending_enquiry_list,name='pending_enquiry_list'),
    path('enquiry_list/',enquiry_list,name='enquiry_list'),
    path('lineitem_list/',lineitem_list,name='enquiry_lineitem_list'),
    path('rfp/<rfp_no>/lineitems/',rfp_lineitem,name='tracker_rfp_lineitem'),
    path('rfp/<rfp_no>/mark_duplicate/',rfp_mark_duplicate,name='rfp_mark_duplicate'),
    path('rfp/<rfp_no>/mark_closed/',rfp_mark_closed,name='rfp_mark_closed'),
]   