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

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins
from rest_framework.renderers import JSONRenderer

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

    if request.method == 'GET':
        expence_list = ClaimDetails.objects.filter(employee=request.user).order_by('-date')
        context['expence_list'] = expence_list

        if type == 'CRM':
            return render(request,"CRM/Claim/claim_history.html",context)

        if type == 'Sourcing':
            return render(request,"Sourcing/Claim/claim_history.html",context)

        if type == 'Sales':
            return render(request,"Sales/Claim/claim_history.html",context)