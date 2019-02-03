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

from Customer.models import *

class CustomerList(generics.GenericAPIView,
                                mixins.ListModelMixin
                                ):
        serializer_class = CustomerSerializer
        queryset = CustomerProfile.objects.all()
        lookup_field = 'id'

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request):
                return self.list(request)

class CustomerContactPersonView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        serializer_class = CustomerContactPersonSerializer
        queryset = CustomerContactPerson.objects.all()
        lookup_field = 'id'

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                customer = CustomerProfile.objects.get(id=self.kwargs['customer_id'])
                return CustomerContactPerson.objects.filter(customer_name = customer)
        
        def get(self,request,customer_id=None):
                return self.list(request) 

        def post(self,request,customer_id=None):
                return self.create(request)

        def perform_create(self,serializer):
                customer = CustomerProfile.objects.get(id=self.kwargs['customer_id'])
                contactperson_id =  self.kwargs['customer_id'] +'P' + str(CustomerContactPerson.objects.count() + 1)
                serializer.save(id=contactperson_id,customer_name=customer,created_by=self.request.user)

class DeliveryContactPersonView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        serializer_class = DeliveryContactPersonSerializer
        queryset = DeliveryContactPerson.objects.all()
        lookup_field = 'id'

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                customer = CustomerProfile.objects.get(id=self.kwargs['customer_id'])
                return DeliveryContactPerson.objects.filter(customer_name = customer)
        
        def get(self,request,customer_id=None,contact_person_id=None):
                return self.list(request) 

        def post(self,request,customer_id=None,contact_person_id=None):
                return self.create(request)

        def perform_create(self, serializer):
                customer = CustomerProfile.objects.get(id=self.kwargs['customer_id'])
                delivery_person_id =  self.kwargs['customer_id'] + 'DP' + str(DeliveryContactPerson.objects.count() + 5)
                serializer.save(id=delivery_person_id,customer_name=customer,created_by=self.request.user)

class SupportingInfoView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        serializer_class = SupportingInfoSerializer
        queryset = CustomerProfile.objects.all()
        lookup_field = 'id'

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return CustomerProfile.objects.filter(id=self.kwargs['customer_id'])
                
        def get(self,request,customer_id=None,contact_person_id=None,delivery_contact_person_id=None):
                return self.list(request) 
                
class StoreSupportingInfoView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        serializer_class = StoreSupportingInfoSerializer
        queryset = CustomerPO.objects.all()
        lookup_field = 'id'

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self,request):
                return self.create(request) 
        
        def perform_create(self, serializer):
                creation_details = CPOCreationDetail.objects.create(created_by=self.request.user)
                customer = CustomerProfile.objects.get(id=self.kwargs['customer_id'])
                customer_contact_person = CustomerContactPerson.objects.get(id=self.kwargs['contact_person_id'])
                delivery_contact_person = DeliveryContactPerson.objects.get(id=self.kwargs['delivery_contact_person_id'])
                serializer.save(customer_name=customer,customer_contact_person=customer_contact_person,delivery_contact_person=delivery_contact_person,cpo_creation_detail=creation_details)