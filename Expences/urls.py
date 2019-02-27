from django.urls import path
from .views import *

urlpatterns = [
    path('new_expence/apply/',new_expence_apply,name='new-expence-apply'),
    path('apply_list/',expence_apply_list,name='expence-apply-list'),
    path('apply_list/<id>/edit/',expense_edit,name='expense-edit'),
    path('apply_list/<id>/delete/',expense_delete,name='expense-delete'),

    #L1 Activity 
    path('1st_stage/pending_approval_list/',pending_approval_list1,name='pending-apprval-list-1'),
    path('1st_stage/<id>/reject/',claim_reject1,name='claim-reject-1'),
    path('1st_stage/<id>/approve/',claim_approve1,name='claim-approve-1'),
    path('1st_stage/approve_all/',claim_approve_all1,name='claim-approve-all-1'),

    #L1 Activity List
    path('1st_stage/approved_list/',approved_list_L1,name='approved-list-L1'),
    path('1st_stage/rejected_list/',rejected_list_L1,name='rejected-list-L2'),


    #L2 Activity
    path('2nd_stage/pending_approval_list/',pending_approval_list2,name='pending-apprval-list-2'),
    path('2nd_stage/<id>/reject/',claim_reject2,name='claim-reject-2'),
    path('2nd_stage/<id>/approve/',claim_approve2,name='claim-approve-2'),
    path('2nd_stage/approve_all/',claim_approve_all2,name='claim-approve-all-2'),

    #L2 Activity List
    path('2nd_stage/approved_list/',approved_list_L2,name='approved-list-L2'),
    path('2nd_stage/rejected_list/',rejected_list_L2,name='rejected-list-L2'),

    #Pending Payment List for Sales / CRM
    path('pending_payment_list/',pending_payment_list,name='pending-payment-list'),
    path('pending_payment_list/<username>/details/',pending_payment_details,name='pending-payment-details'),

    #Payment Completion
    path('pending_payment_list/<username>/payment_completion/',pending_payment_completion,name='pending-payment-completion'),
]   
