from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('',ApplicableLeavesViewSet)

urlpatterns = [
    #path('api/applicable_leave/',include(router.urls)),
    #path('api/leave/list/',ApplicableLeavesList, name='applicable-leave-list'),
    
    #admin
    ##Applicable Leave Management
    path('applicable_leave/',ApplicableLeavesListView.as_view()),
    path('applicable_leave/<id>/',ApplicableLeavesListView.as_view()),
    ##All Leave
    path('admin/leave_applications/list/',AllLeaveApplicationsList.as_view()),
    path('admin/leave_applications/<id>/details/',AllLeaveApplicationsList.as_view()),
    #leave cancellation
    path('admin/leave_applications/<id>/details/cancel/',LeaveCancellation.as_view()),


    #User
    path('user/applicable_leave/',UserApplicableLeave.as_view()),
    path('user/leave_request/create/',NewLeaveRequest.as_view()),

    #AppliedList for user
    path('user/leave_request/list/',UserAppliedLeave.as_view()),
    
    #Manager
    #Pending Approval List
    path('pending_approval/list/',PendingApprovalLeaveList.as_view()),
    path('pending_approval/list/<id>/',PendingApprovalLeaveList.as_view()),

    #Manager
    #Approve Application
    path('pending_approval/<id>/approve/',LeaveApprove.as_view()),

    #Reject Application
    path('pending_approval/<id>/reject/',LeaveReject.as_view()),
]