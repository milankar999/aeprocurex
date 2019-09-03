from django.views.generic import View
from django.shortcuts import render
from rest_framework import viewsets
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
import io
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from State.models import StateList
from RFP.models import *
from Sourcing.models import *
import random
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.db.models import F
from django.db.models import Sum

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins
from rest_framework.renderers import JSONRenderer
from django.db.models import Q


class NewClaimViewSet(generics.GenericAPIView,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin
                        ):

    serializer_class = NewClaimSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return ClaimDetails.objects.filter(employee=self.request.user)

    authentication_classes=[TokenAuthentication ,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self,request):
        return self.create(request)

    def perform_create(self,serializer):
        serializer.save(employee=self.request.user)

    def put(self,request,id=None):
        claim = ClaimDetails.objects.get(id=id)
        if claim.employee != self.request.user:
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
        if claim.status == 'Requested' or claim.status == 'Rejected':
            return self.partial_update(request)
        else:
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
    
    def delete(self,request,id=None):
        claim = ClaimDetails.objects.get(id=id)
        if claim.employee != self.request.user:
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
        if claim.status == 'Requested' or claim.status == 'Rejected':
            return self.destroy(request,id)
        else:
            return JsonResponse({"Message" : "Not Allowed"}, safe=False)
    
#Claim Types - List
class ClaimTypesViewSet(generics.GenericAPIView,
                        mixins.ListModelMixin
                        ):
    queryset = ThirdClaimTypes.objects.all()
    serializer_class = ClaimTypesSerializer
    lookup_field = 'claim_types3'

    def get(self,request):
        return self.list(request)    



##With out api

@login_required(login_url="/employee/login/")
def new_expence_apply(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == 'GET':        
        claim_types = ThirdClaimTypes.objects.all()
        context['claim_types'] = claim_types

        if type == 'CRM':
            return render(request,"CRM/Claim/claim_application.html",context)

        if type == 'Sourcing':
            return render(request,"Sourcing/Claim/claim_application.html",context)

        if type == 'Sales':
            return render(request,"Sales/Claim/claim_application.html",context)

    try:
        if request.method == 'POST' and request.FILES['supporting_document']:
            data = request.POST
            myfile = request.FILES['supporting_document']

            ClaimDetails.objects.create(
                employee=request.user,
                claim_type=ThirdClaimTypes.objects.get(claim_type3 = data['expence_type']),
                description=data['description'],
                total_basic_amount = data['basic_value'],
                applicable_gst_value = data['gst_value'],
                date =data['date'],
                document = myfile,
                )
            return HttpResponseRedirect(reverse('expence-apply-list'))
    except:
            if request.method == 'POST':
                data = request.POST

                ClaimDetails.objects.create(
                    employee=request.user,
                    claim_type=ThirdClaimTypes.objects.get(claim_type3 = data['expence_type']),
                    description=data['description'],
                    total_basic_amount = data['basic_value'],
                    applicable_gst_value = data['gst_value'],
                    date =data['date'],
                    )
                return HttpResponseRedirect(reverse('expence-apply-list'))        

@login_required(login_url="/employee/login/")
def expence_apply_list(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        expence_list = ClaimDetails.objects.filter(employee=request.user,status='Requested').order_by('-date')
        context['expence_list'] = expence_list

        if type == 'CRM':
            return render(request,"CRM/Claim/claim_history.html",context)

        if type == 'Sourcing':
            return render(request,"Sourcing/Claim/claim_history.html",context)

        if type == 'Sales':
            return render(request,"Sales/Claim/claim_history.html",context)

@login_required(login_url="/employee/login/")
def expense_edit(request,id=None):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        expense = ClaimDetails.objects.get(id=id)
        #.values(
        #    'claim_type__claim_type3',
        #    'description',
        #    'total_basic_amount',
        #    'applicable_gst_value',
        #    'date',
        #    'document')
        context['expense'] = expense

        claim_types = ThirdClaimTypes.objects.all()
        context['claim_types'] = claim_types

        if type == 'CRM':
            return render(request,"CRM/Claim/claim_edit.html",context)

        if type == 'Sourcing':
            return render(request,"Sourcing/Claim/claim_edit.html",context)

        if type == 'Sales':
            return render(request,"Sales/Claim/claim_edit.html",context)

    try:
        if request.method == 'POST' and request.FILES['supporting_document']:
            data = request.POST
            myfile = request.FILES['supporting_document']

            claim_object = ClaimDetails.objects.get(id = id) 

            claim_object.claim_type=ThirdClaimTypes.objects.get(claim_type3 = data['expence_type'])
            claim_object.description=data['description']
            claim_object.total_basic_amount = data['basic_value']
            claim_object.applicable_gst_value = data['gst_value']
            
            if data['date'] != '':
                claim_object.date = data['date']
            
            claim_object.document = myfile
            claim_object.status = 'Requested'

            claim_object.save()
                
            return HttpResponseRedirect(reverse('expence-apply-list'))
    
    except:
            if request.method == 'POST':
                data = request.POST
                print('date' + data['date'])
                claim_object = ClaimDetails.objects.get(id = id) 
                claim_object.claim_type=ThirdClaimTypes.objects.get(claim_type3 = data['expence_type'])
                claim_object.description=data['description']
                claim_object.total_basic_amount = data['basic_value']
                claim_object.applicable_gst_value = data['gst_value']

                if data['date'] != '':
                    claim_object.date = data['date']

                claim_object.status = 'Requested'
                
                claim_object.save()

                return HttpResponseRedirect(reverse('expence-apply-list'))       

#Expense Delete
@login_required(login_url="/employee/login/")
def expense_delete(request,id=None):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        expense = ClaimDetails.objects.get(id=id)
        context['expense'] = expense

        claim_types = ThirdClaimTypes.objects.all()
        context['claim_types'] = claim_types

        if type == 'CRM':
            return render(request,"CRM/Claim/claim_delete.html",context)

        if type == 'Sourcing':
            return render(request,"Sourcing/Claim/claim_delete.html",context)

        if type == 'Sales':
            return render(request,"Sales/Claim/claim_delete.html",context)

    if request.method == 'POST':
        expense = ClaimDetails.objects.get(id=id)
        expense.delete()

        return HttpResponseRedirect(reverse('expence-apply-list'))  

#Lavel1 Approval List
@login_required(login_url="/employee/login/")
def pending_approval_list1(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if u.profile.claim_user_type != 'L1':
        context['error'] = 'You are Not The Right Person For Viewing This Page'
        return render(request,"Sales/error.html",context)

    if request.method == 'GET':
        user_list = User.objects.all()
        context['user_list'] = user_list

        expence_list = ClaimDetails.objects.filter(status = 'Requested').values(
            'id',
            'claim_type',
            'employee__username',
            'description',
            'date',
            'total_basic_amount',
            'applicable_gst_value',
            'document').order_by('-date')
        context['expense_list'] = expence_list

        date_object = ClaimDetails.objects.filter(status = 'Requested').values('date').order_by('-date').distinct()
        context['date_object'] = date_object

        user_date_object = ClaimDetails.objects.filter(status = 'Requested').values('date','employee__username','employee__first_name','employee__last_name').order_by('-date').distinct().annotate(Count("date"))
        context['user_date_object'] = user_date_object

        print(user_date_object)

        if type == 'Sales':
            return render(request,"Sales/Claim/Approval_List1/claim_approval_list1.html",context)

#Expense Reject
@login_required(login_url="/employee/login/")
def claim_reject1(request,id=None):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'POST':
        claim_object = ClaimDetails.objects.get(id=id)
        claim_object.status = 'Rejected1'
        claim_object.save()

        return HttpResponseRedirect(reverse('pending-apprval-list-1'))  

#Expense Approve
@login_required(login_url="/employee/login/")
def claim_approve1(request,id=None):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'POST':
        claim_object = ClaimDetails.objects.get(id=id)
        claim_object.status = 'Approved1'
        claim_object.save()

        return HttpResponseRedirect(reverse('pending-apprval-list-1'))  

#Expense Approve ALL
@login_required(login_url="/employee/login/")
def claim_approve_all1(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'POST':
        claim_object = ClaimDetails.objects.filter(status='Requested')

        for claim in claim_object:
            claim.status = 'Approved1'
            claim.save()

        return HttpResponseRedirect(reverse('pending-apprval-list-1'))  



#L2 Approval
#Lavel1 Approval List
@login_required(login_url="/employee/login/")
def pending_approval_list2(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if u.profile.claim_user_type != 'L2':
        context['error'] = 'You are Not The Right Person For Viewing This Page'
        return render(request,"Sales/error.html",context)

    if request.method == 'GET':
        user_list = User.objects.all()
        context['user_list'] = user_list

        expence_list = ClaimDetails.objects.filter(status = 'Approved1').values(
            'id',
            'claim_type',
            'employee__username',
            'description',
            'date',
            'total_basic_amount',
            'applicable_gst_value',
            'document').order_by('-date')
        context['expense_list'] = expence_list

        date_object = ClaimDetails.objects.filter(status = 'Approved1').values('date').order_by('-date').distinct()
        context['date_object'] = date_object

        user_date_object = ClaimDetails.objects.filter(status = 'Approved1').values('date','employee__username','employee__first_name','employee__last_name').order_by('-date').distinct().annotate(Count("date"))
        context['user_date_object'] = user_date_object

        print(user_date_object)

        if type == 'Sales':
            return render(request,"Sales/Claim/Approval_List2/claim_approval_list2.html",context)

#Expense Reject
@login_required(login_url="/employee/login/")
def claim_reject2(request,id=None):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'POST':
        claim_object = ClaimDetails.objects.get(id=id)
        claim_object.status = 'Rejected2'
        claim_object.save()

        return HttpResponseRedirect(reverse('pending-apprval-list-2'))  

#Expense Approve
@login_required(login_url="/employee/login/")
def claim_approve2(request,id=None):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'POST':
        claim_object = ClaimDetails.objects.get(id=id)
        claim_object.status = 'Approved2'
        claim_object.save()

        return HttpResponseRedirect(reverse('pending-apprval-list-2'))  

#Expense Approve ALL
@login_required(login_url="/employee/login/")
def claim_approve_all2(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'POST':
        claim_object = ClaimDetails.objects.filter(status='Approved1')

        for claim in claim_object:
            claim.status = 'Approved2'
            claim.save()

        return HttpResponseRedirect(reverse('pending-apprval-list-2'))

#Lavel1 Approval List
@login_required(login_url="/employee/login/")
def approved_list_L1(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        expence_list = ClaimDetails.objects.filter(employee=request.user,status='Approved1').order_by('-date')
        context['expence_list'] = expence_list

        if type == 'CRM':
            return render(request,"CRM/Claim/approve1.html",context)

        if type == 'Sourcing':
            return render(request,"Sourcing/Claim/approve1.html",context)

        if type == 'Sales':
            return render(request,"Sales/Claim/approve1.html",context)

#Lavel1 Rejected List
@login_required(login_url="/employee/login/")
def rejected_list_L1(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        expence_list = ClaimDetails.objects.filter(employee=request.user,status='Rejected1').order_by('-date')
        context['expence_list'] = expence_list

        if type == 'CRM':
            return render(request,"CRM/Claim/rejected1.html",context)

        if type == 'Sourcing':
            return render(request,"Sourcing/Claim/rejected1.html",context)

        if type == 'Sales':
            return render(request,"Sales/Claim/rejected1.html",context)

#Lavel2 Approval List
@login_required(login_url="/employee/login/")
def approved_list_L2(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        expence_list = ClaimDetails.objects.filter(employee=request.user,status='Approved2').order_by('-date')
        context['expence_list'] = expence_list

        if type == 'CRM':
            return render(request,"CRM/Claim/approve2.html",context)

        if type == 'Sourcing':
            return render(request,"Sourcing/Claim/approve2.html",context)

        if type == 'Sales':
            return render(request,"Sales/Claim/approve2.html",context)

#Lavel1 Rejected List
@login_required(login_url="/employee/login/")
def rejected_list_L2(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        expence_list = ClaimDetails.objects.filter(employee=request.user,status='Rejected2').order_by('-date')
        context['expence_list'] = expence_list

        if type == 'CRM':
            return render(request,"CRM/Claim/rejected2.html",context)

        if type == 'Sourcing':
            return render(request,"Sourcing/Claim/rejected2.html",context)

        if type == 'Sales':
            return render(request,"Sales/Claim/rejected2.html",context)

#Pending Payment List
@login_required(login_url="/employee/login/")
def pending_payment_list(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        payment_list = ClaimDetails.objects.filter(status='Approved2').values('employee__first_name','employee__last_name','employee__username').annotate(Sum('total_basic_amount'),Sum('applicable_gst_value'))
        context['payment_list'] = payment_list

        if type == 'Sales':
            return render(request,"Sales/Claim/pending_payment.html",context)

        if type == 'CRM':
            if u.profile.claim_user_type != 'Admin':
                context['error'] = 'You are Not The Right Person For Viewing This Page'
                return render(request,"CRM/error.html",context)
            return render(request,"CRM/Claim/pending_payment.html",context)

#Pending Payment details
@login_required(login_url="/employee/login/")
def pending_payment_details(request, username=None):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        emp = User.objects.get(username=username)
        expence_list = ClaimDetails.objects.filter(employee=emp,status='Approved2').order_by('-date')
        context['expence_list'] = expence_list
        context['user'] = emp.first_name + ' ' + emp.last_name
        context['username'] = emp.username

        if type == 'CRM':
            if u.profile.claim_user_type != 'Admin':
                context['error'] = 'You are Not The Right Person For Viewing This Page'
                return render(request,"CRM/error.html",context)
            return render(request,"CRM/Claim/pending_payment_details.html",context)

        if type == 'Sales':
            return render(request,"Sales/Claim/pending_payment_details.html",context)

#Pending Payment Completion
@login_required(login_url="/employee/login/")
def pending_payment_completion(request, username=None):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if u.profile.claim_user_type != 'Admin':
        context['error'] = 'You are Not The Right Person For Viewing This Page'
        return render(request,"CRM/error.html",context)

    if request.method == 'POST':
        emp = User.objects.get(username=username)
        expence_list = ClaimDetails.objects.filter(employee=emp,status='Approved2').order_by('-date')
        for item in expence_list:
            print(item)
            item.status = 'Paid'
            item.save()
        
        return HttpResponseRedirect(reverse('pending-payment-list'))

#Individual Payment Status
@login_required(login_url="/employee/login/")
def individual_payment_status(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        context['expense_details'] = ClaimDetails.objects.filter(employee=request.user).values(
            'status').annotate(
                Sum('total_basic_amount'),
                Sum('applicable_gst_value'))
        
        if type == 'Sales':
            return render(request,"Sales/Claim/individual_payment_status.html",context)
        
        if type == 'Sourcing':
            return render(request,"Sourcing/Claim/individual_payment_status.html",context)
        
        if type == 'CRM':
            return render(request,"CRM/Claim/individual_payment_status.html",context)

#All expence list
@login_required(login_url="/employee/login/")
def all_expence_list(request):
    context={}
    context['expence'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type   
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        user_list = User.objects.all()
        context['user_list'] = user_list

        expence_list = ClaimDetails.objects.filter(Q(status = 'Requested')|Q(status = 'Approved1')|Q(status = 'Approved2')|Q(status = 'Paid')).values(
            'id',
            'claim_type',
            'employee__username',
            'description',
            'date',
            'total_basic_amount',
            'applicable_gst_value',
            'document').order_by('-date')
        context['expense_list'] = expence_list

        date_object = ClaimDetails.objects.filter(Q(status = 'Requested')|Q(status = 'Approved1')|Q(status = 'Approved2')|Q(status = 'Paid')).values('date').order_by('-date').distinct()
        context['date_object'] = date_object

        user_date_object = ClaimDetails.objects.filter(Q(status = 'Requested')|Q(status = 'Approved1')|Q(status = 'Approved2')|Q(status = 'Paid')).values('date','employee__username','employee__first_name','employee__last_name').order_by('-date').distinct().annotate(Count("date"))
        context['user_date_object'] = user_date_object

        if type == 'Accounts':
            return render(request,"Accounts/Claim/claim_list.html",context)