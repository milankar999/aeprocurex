from django.urls import path
from .views import *

urlpatterns = [
    path('pending_enquiry_list/',pending_enquiry_list,name='pending_enquiry_list'),
    path('enquiry_list/',enquiry_list,name='enquiry_list'),
    path('lineitem_list/',lineitem_list,name='enquiry_lineitem_list'),
    path('rfp/<rfp_no>/lineitems/',rfp_lineitem,name='tracker_rfp_lineitem'),
    path('rfp/<rfp_no>/mark_duplicate/',rfp_mark_duplicate,name='rfp_mark_duplicate'),
    path('rfp/<rfp_no>/mark_closed/',rfp_mark_closed,name='rfp_mark_closed'),
    path('rfp/<rfp_no>/reassign/',rfp_reassign,name='rfp_reassign'),
    path('rfp/<rfp_no>/restore/',rfp_restore,name='rfp_restore'),

    #Edit enquiry
    path('rfp/<rfp_no>/edit_enquiry/',rfp_edit,name='rfp_edit'),
    path('rfp/<rfp_no>/edit_enquiry/save_changes/',rfp_save_changes,name='rfp_save_changes'),
    path('rfp/<rfp_no>/edit_enquiry/<lineitem>/lineitem_edit/',rfp_lineitem_edit,name='rfp_lineitem_edit'),


    #Pending Slider
    path('pending_enquiry_slider/',pending_enquiry_slider,name='pending_enquiry_slider'),
]   