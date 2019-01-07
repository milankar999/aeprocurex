from django.views.generic import View
from django.shortcuts import render
from rest_framework import viewsets
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
import io

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins
from rest_framework.renderers import JSONRenderer

class ApplicableLeavesViewSet(viewsets.ModelViewSet):
    queryset = ApplicableLeaves.objects.all()
    serializer_class = ApplicableLeavesSerializer

@csrf_exempt
def ApplicableLeavesList(request):
    authentication_classes = [TokenAuthentication ,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    if request.method=='GET':
        leave_list = ApplicableLeaves.objects.all()
        serializer = ApplicableLeavesSerializer(leave_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = ApplicableLeavesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400) 

#Applicable Leave Management 
class ApplicableLeavesListView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin
                                ):
    serializer_class = ApplicableLeavesSerializer
    queryset = ApplicableLeaves.objects.all()
    lookup_field = 'id'

    #Check Authentications
    authentication_classes=[TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated,]


    def get(self,request,id=None):
        if self.request.user.profile.hr_user_type == "Employee":
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self,request):
        if self.request.user.profile.hr_user_type == "Employee":
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
        return self.create(request)

    def put(self,request,id=None):
        if self.request.user.profile.hr_user_type == "Employee":
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
        return self.partial_update(request)

#New Leave Request
class NewLeaveRequest(generics.GenericAPIView,
                                mixins.CreateModelMixin,
                                ):
    lookup_field = 'id'

    authentication_classes=[TokenAuthentication ,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        return NewLeaveSerializer

    def post(self,request):
        data = request.data
        applicable_leaves = ApplicableLeaves.objects.get(employee = self.request.user)
        print(data)
        if data['leave_type'] == 'Annual':
            if(float(data['no_of_days'])>float(applicable_leaves.leaves)):
                return JsonResponse({"Message" : "Unavailable"}, safe=False)
            else:
                applicable_leaves.leaves = float(applicable_leaves.leaves) - float(data['no_of_days'])
                applicable_leaves.save()
                return self.create(request)               
        elif data['leave_type'] == 'LOP':
            return self.create(request)
        else:
            return JsonResponse({"Message" : "Wrong Information"}, safe=False)

        
    def perform_create(self,serializer):
        serializer.save(employee=self.request.user)

#Get the applicable leaves for loggedin user
class UserApplicableLeave(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                ):
    #Check Authentications
    authentication_classes=[TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated,]

    lookup_field = 'id'
    serializer_class = UserApplicableLeavesSerializer

    def get_queryset(self):
        return ApplicableLeaves.objects.filter(employee = self.request.user)

    def get(self,request): 
        return self.list(request)

#Get Applied Leave History
class UserAppliedLeave(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin
                                ):

    #Check Authentications
    authentication_classes=[TokenAuthentication ,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = AppliedLeaveSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return LeaveApplication.objects.filter(employee = self.request.user).order_by('-created_at')

    def get(self,request):
        return self.list(request)

class PendingApprovalLeaveList(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin):

    serializer_class = PendingApprovalLeaveSerializer
    lookup_field = 'id'
    
    authentication_classes = [TokenAuthentication ,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LeaveApplication.objects.filter(status = 'Requested')

    def get(self,request,id=None):
        if self.request.user.profile.hr_user_type != 'Manager':
            return JsonResponse({"Message" : "You are not right person"}, safe=False)
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

#Leave Approve
class LeaveApprove(generics.GenericAPIView,
                    mixins.CreateModelMixin,):
    authentication_classes = [TokenAuthentication ,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ApprovalSerializer

    def post(self,request,id=None):
        if self.request.user.profile.hr_user_type != 'Manager':
            return JsonResponse({"Message" : "You are not right person"}, safe=False)
        application = LeaveApplication.objects.get(id=id)
        if application.status != 'Requested':
            return JsonResponse({"Message" : "Wrong information"}, safe=False)
        application.status = 'Approved'
        application.save()
        return JsonResponse({"Message" : "Success"}, safe=False)
        
#Leave Reject
class LeaveReject(generics.GenericAPIView,
                    mixins.CreateModelMixin,):
    authentication_classes = [TokenAuthentication ,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ApprovalSerializer

    def post(self,request,id=None):
        if self.request.user.profile.hr_user_type != 'Manager':
            return JsonResponse({"Message" : "You are not right person"}, safe=False)
        application = LeaveApplication.objects.get(id=id)
        if application.status != 'Requested':
            return JsonResponse({"Message" : "Wrong information"}, safe=False)
        
        #Increase applicable leave
        applicable_leave = ApplicableLeaves.objects.get(employee=application.employee)
        applicable_leave.leaves = applicable_leave.leaves + application.no_of_days
        applicable_leave.save()

        application.status = 'Rejected'
        application.save()

        return JsonResponse({"Message" : "Success"}, safe=False)

#Admin
##All Leave Application Listing
class AllLeaveApplicationsList(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin):
    authentication_classes = [TokenAuthentication ,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AllLeaveApplicationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return LeaveApplication.objects.all()

    def get(self,request,id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)
    
#Leave cancellation
class LeaveCancellation(generics.GenericAPIView,
                    mixins.CreateModelMixin,):
    authentication_classes = [TokenAuthentication ,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ApprovalSerializer

    def post(self,request,id=None):
        if self.request.user.profile.hr_user_type != 'Admin':
            return JsonResponse({"Message" : "You are not right person"}, safe=False)
        application = LeaveApplication.objects.get(id=id)

        if application.status == 'Approved' or application.status == 'Requested':
            #if application.start_date
            applicable_leave = ApplicableLeaves.objects.get(employee=application.employee)
            applicable_leave.leaves = applicable_leave.leaves + application.no_of_days
            applicable_leave.save()
            application.status = 'Cancelled'
            application.save()
            print('sdf')
            return JsonResponse({"Message" : "Success"}, safe=False)

        else:
            return JsonResponse({"Message" : "Wrong information"}, safe=False)
        
        #Increase applicable leave
        