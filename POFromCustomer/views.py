from django.views.generic import View
from django.contrib.auth.models import User
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

from rest_framework.response import Response

from Customer.models import *
from Quotation.models import *

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

        def post(self,request,customer_id=None,contact_person_id=None,delivery_contact_person_id=None):
                return self.create(request) 
        
        def perform_create(self, serializer):
                customer = CustomerProfile.objects.get(id=self.kwargs['customer_id'])
                customer_contact_person = CustomerContactPerson.objects.get(id=self.kwargs['contact_person_id'])
                delivery_contact_person = DeliveryContactPerson.objects.get(id=self.kwargs['delivery_contact_person_id'])
                creation_details = CPOCreationDetail.objects.create(created_by=self.request.user)
                
                serializer.save(
                        customer = customer,
                        customer_contact_person = customer_contact_person,
                        delivery_contact_person = delivery_contact_person,
                        cpo_creation_detail = creation_details
                        )

class CPOQuotationSelectionView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        #serializer_class = CPOQuotationSelectionSerializer
        #queryset = QuotationTracker.objects.all()
        #lookup_field = 'quotation_no'

        def get_serializer_class(self):
                if self.request.method == 'GET':
                        return CPOQuotationSelectionSerializer

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                cpo_obj = CustomerPO.objects.get(id=self.kwargs['cpo_id'])
                return QuotationTracker.objects.filter(customer=cpo_obj.customer)
                
        def get(self,request,cpo_id=None):
                return self.list(request) 

        

class CPOQuotationDetailsView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin):
        
        serializer_class = CPOQuotationDetailsSerializer

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                quotation_obj = QuotationTracker.objects.get(quotation_no=self.kwargs['quotation_no'])
                return QuotationLineitem.objects.filter(quotation=quotation_obj)
                
        def get(self,request,quotation_no=None):
                return self.list(request) 

class CPOQuotationSelectedView(APIView):
        """
        A view that can accept POST requests with JSON content.
        """
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None):
                try:
                        for q_no in request.data['quotation_no']:
                                print(q_no)
                                CPOSelectedQuotation.objects.create(
                                        quotation=QuotationTracker.objects.get(quotation_no=q_no),
                                        customer_po=CustomerPO.objects.get(id=cpo_id))
                        return Response({'Message': 'Success'})
                except:
                        return Response({'Message': 'Error Occured'})

class CPOQuotationProductListView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin):

        serializer_class = CPOQuotationProductListSerializer

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                selected_quotation_list = CPOSelectedQuotation.objects.filter(customer_po=CustomerPO.objects.get(id=self.kwargs['cpo_id']))
                i = 1
                for quotation in selected_quotation_list:
                        if i == 1:
                                quotation_lineitems = QuotationLineitem.objects.filter(quotation=quotation.quotation)
                                i = i + 1 
                        else:
                                quotation_lineitems = quotation_lineitems.union(QuotationLineitem.objects.filter(quotation=quotation.quotation))
                return quotation_lineitems

        def get(self, request, cpo_id = None):
                return self.list(request)


class CPOQuotationProductSelectedView(APIView):
        """
        A view that can accept POST requests with JSON content.
        """
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None):
                try :
                        cpo = CustomerPO.objects.get(id=cpo_id)
                        for item in request.data['quotation_lineitems']:
                                print(item)
                                
                                quotation_lineitem_obj = QuotationLineitem.objects.get(id = item)
                                CPOLineitem.objects.create(
                                        cpo = cpo,
                                        quotation_lineitem = quotation_lineitem_obj,
                                        product_title = quotation_lineitem_obj.product_title,
                                        description = quotation_lineitem_obj.description,
                                        model = quotation_lineitem_obj.model,
                                        brand = quotation_lineitem_obj.brand,
                                        product_code = quotation_lineitem_obj.product_code,
                                        part_no= quotation_lineitem_obj.part_number,
                                        hsn_code = quotation_lineitem_obj.hsn_code,
                                        pack_size = quotation_lineitem_obj.pack_size,
                                        gst = quotation_lineitem_obj.gst,
                                        quantity = quotation_lineitem_obj.quantity,
                                        uom = quotation_lineitem_obj.uom,
                                        unit_price = quotation_lineitem_obj.unit_price
                                        )
                        return Response({'Message': 'Success'})
                except:
                        return Response({'Message': 'Error Occured'})

class CPOSelectedProductListView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin):

        serializer_class = CPOSelectedProductListSerializer

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return CPOLineitem.objects.filter(cpo=CustomerPO.objects.get(id=self.kwargs['cpo_id']))

        def get(self, request, cpo_id = None):
                return self.list(request)

#Add New Lineitem
class CPOAddNewItemView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                ):
        serializer_class = CPONewProductListSerializer
        lookup_field = 'id'

        queryset = CPOLineitem.objects.all()

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self,request,cpo_id=None,id=None):
                return self.create(request)

        def perform_create(self,serializer):
                cpo = CustomerPO.objects.get(id=self.kwargs['cpo_id'])
                serializer.save(cpo=cpo)



#Edit Selected Lineitem
class CPOSelectedProductEditView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin
                                ):
        serializer_class = CPOSelectedProductEditSerializer
        lookup_field = 'id'

        queryset = CPOLineitem.objects.all()

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,cpo_id=None,id=None):
                return self.retrieve(request, id)

        def put(self,request,cpo_id=None,id=None):
                return self.partial_update(request)

#Launch CPO
class CPOlaunch(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None):
                cpo = CustomerPO.objects.get(id = cpo_id)
                cpo.status = 'created'
                cpo.save()
                return Response({'Message': 'Success'})


#CPO Approval List
class CPOApprovalListView(generics.GenericAPIView,
                                mixins.ListModelMixin,):
        serializer_class = CPOPendingApprovalListSerializer
        lookup_field = 'id'

        queryset = CPOLineitem.objects.all()

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return(CustomerPO.objects.filter(status='created'))

        def get(self,request):
                return self.list(request)

#CPO Approval List
class CPOApprovalLineitemsView(generics.GenericAPIView,
                                mixins.ListModelMixin,):
        serializer_class = CPOPendingApprovalLineitemSerializer
        lookup_field = 'id'

        queryset = CPOLineitem.objects.all()

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return(CPOLineitem.objects.filter(cpo=CustomerPO.objects.get(id=self.kwargs['cpo_id'])))

        def get(self,request,cpo_id):
                return self.list(request)

#CPO Approval Info
class CPOApprovalInfoView(generics.GenericAPIView,
                                mixins.RetrieveModelMixin,):
        serializer_class = CPOApprovalInfoSerializer
        lookup_field = 'id'

        queryset = CustomerPO.objects.all()

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,id):
                return self.retrieve(request, id)

#Sourcing Person List
class ByuerListView(generics.GenericAPIView,
                        mixins.ListModelMixin,):
        serializer_class = CPOBuyerListSerializer

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return(User.objects.filter(profile__type='Sourcing'))
        
        def get(self,request):
                return self.list(request)

#Approve Customer PO
class CPOApprove(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None):
                try:
                        assign_to = CPOAssign.objects.create(assign_to=User.objects.get(username=request.data['assign_to']))
                        cpo = CustomerPO.objects.get(id = cpo_id)
                        cpo.status = 'approved'
                        cpo.cpo_assign_detail = assign_to
                        cpo.save()
                        return Response({'Message': 'Success'})
                
                except:
                        return Response({'Message': 'Error'})

#Approve Customer PO
class CPOReject(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None):
                try:                        
                        cpo = CustomerPO.objects.get(id = cpo_id)
                        cpo.status = 'rejected'
                        cpo.rejection_reason = request.data['rejection_reason']
                        cpo.save()
                        return Response({'Message': 'Success'})
                
                except: 
                        return Response({'Message': 'Error'})

#CPO Rejected List
class CPORejectedListView(generics.GenericAPIView,
                                mixins.ListModelMixin,):
        serializer_class = CPORejectedListSerializer
        lookup_field = 'id'

        queryset = CPOLineitem.objects.all()

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return(CustomerPO.objects.filter(status='rejected'))

        def get(self,request):
                return self.list(request)

#CPO Rejected Lineitems
class CPORejectedLineitemsView(generics.GenericAPIView,
                                mixins.ListModelMixin,):
        serializer_class = CPORejectedLineitemSerializer
        lookup_field = 'id'

        queryset = CPOLineitem.objects.all()

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return(CPOLineitem.objects.filter(cpo=CustomerPO.objects.get(id=self.kwargs['cpo_id'])))

        def get(self,request,cpo_id):
                return self.list(request)

#Rejected Item Edit
class CPORejectedProductEditView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin
                                ):
        serializer_class = CPORejectedProductEditSerializer
        lookup_field = 'id'

        queryset = CPOLineitem.objects.all()

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,cpo_id=None,id=None):
                return self.retrieve(request, id)

        def put(self,request,cpo_id=None,id=None):
                return self.partial_update(request)

        def delete(self,request,cpo_id=None,id=None):
                return self.destroy(request,id)


#Supporting info edit
class CPORejectedSupportingInfoEditView(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin):
        serializer_class = CPORejectedSupportingInfoEditSerializer
        lookup_field = 'id'

        queryset = CustomerPO.objects.all()

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,id=None):
                return self.retrieve(request,id)
        
        def put(self,request,id=None):
                return self.partial_update(request)

#Deactivate / Delete  CPO
class RejectedCPODelete(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, id = None):
                cpo = CustomerPO.objects.get(id = id)
                cpo.status = 'Deleted'
                cpo.save()
                return Response({'Message': 'Success'})

#Mark Resolved
class RejectedCPOResolve(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, id = None):
                cpo = CustomerPO.objects.get(id = id)
                cpo.status = 'created'
                cpo.save()
                return Response({'Message': 'Success'})









###Without API
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from Employee.models import *
from .models import *
from State.models import *
from Customer.models import *
from django.core.mail import send_mail, EmailMessage
from django.core import mail
import random
from django.conf import settings
from django.db.models import F
from POForVendor.models import *
from django.db.models import Count

#Customer Selection
@login_required(login_url="/employee/login/")
def cpo_create_customer_selection(request):
        context={}
        context['po'] = 'active'

        if request.method == "GET":
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                customer = CustomerProfile.objects.all()
                context['CustomerList'] = customer
                state = StateList.objects.all()
                context['StateList'] = state
        
                if type == 'CRM':
                        return render(request,"CRM/PO/customer_selection.html",context)

        if request.method == "POST":
                user = User.objects.get(username=request.user)
                data = request.POST
                customer_id = 'C1' + str(format(CustomerProfile.objects.count() + 1, '04d'))
                print(customer_id)
                cust = CustomerProfile.objects.create(id=customer_id,name=data['name'],location=data['location'],code=data['code'],address=data['address'],city=data['city'],state=data['state'],pin=data['pin'],country=data['country'],office_email1=data['officeemail1'],office_email2=data['officeemail2'],office_phone1=data['officephone1'],office_phone2=data['officephone2'],gst_number=data['GSTNo'],vendor_code=data['VendorCode'],payment_term=data['PaymentTerm'],inco_term=data['IncoTerm'],created_by=user)
                if cust:
                        u = User.objects.get(username=request.user)
                        type = u.profile.type
                        context['login_user_name'] = u.first_name + ' ' + u.last_name
                        customer = CustomerProfile.objects.all()
                        context['CustomerList'] = customer
                        state = StateList.objects.all()
                        context['StateList'] = state
                        context['message'] = 'Successfully registered ' + data['name']
                        context['message_type'] = 'success'
                        
                        if type == 'CRM':
                                return render(request,"CRM/PO/customer_selection.html",context)
        
                else:
                        u = User.objects.get(username=request.user)
                        type = u.profile.type
                        context['login_user_name'] = u.first_name + ' ' + u.last_name
                        customer = CustomerProfile.objects.all()
                        context['CustomerList'] = customer
                        state = StateList.objects.all()
                        context['StateList'] = state
                        context['message'] = 'Something went wrong'
                        context['message_type'] = 'danger'
                        
                        if type == 'CRM':
                                return render(request,"CRM/PO/customer_selection.html",context)

#Customer Contact Person / Requester Selection
@login_required(login_url="/employee/login/")
def cpo_create_contact_person_selection(request, cust_id=None):
        context={}
        context['po'] = 'active'

        if request.method == "GET":
                user = User.objects.get(username=request.user)
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                ContactPerson = CustomerContactPerson.objects.filter(customer_name__pk=cust_id)
                context['ContactPerson'] = ContactPerson
                customer = CustomerProfile.objects.get(id=cust_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = cust_id

                if type == 'CRM':
                        return render(request,"CRM/PO/contact_person_selection.html",context)

        if request.method == "POST":
                user = User.objects.get(username=request.user)
                data = request.POST
                customer = CustomerProfile.objects.get(id=cust_id)
                contactperson_id =  cust_id +'P' + str(CustomerContactPerson.objects.count() + 1)
                cp = CustomerContactPerson.objects.create(id=contactperson_id,name=data['name'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],customer_name=customer,created_by=user)
                if cp:
                        context['message'] = 'Successfully registered ' + data['name']
                        context['message_type'] = 'success'
                else:
                        context['message'] = 'Something went wrong'
                        context['message_type'] = 'danger'
      
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                ContactPerson = CustomerContactPerson.objects.filter(customer_name__pk=cust_id)
                context['ContactPerson'] = ContactPerson
                customer = CustomerProfile.objects.get(id=cust_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = cust_id
        
                if type == 'CRM':
                        return render(request,"CRM/PO/contact_person_selection.html",context)

#Receiver Selection
@login_required(login_url="/employee/login/")
def cpo_create_receiver_selection(request, cust_id=None,contact_person_id=None):
        context={}
        context['po'] = 'active'

        if request.method == "GET":
                user = User.objects.get(username=request.user)
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                receiver = DeliveryContactPerson.objects.filter(customer_name__pk=cust_id)
                context['receiver'] = receiver
                customer = CustomerProfile.objects.get(id=cust_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = cust_id
                context['ContactPersonID'] = contact_person_id

                if type == 'CRM':
                        return render(request,"CRM/PO/receiver_selection.html",context)

        if request.method == "POST":
                user = User.objects.get(username=request.user)
                data = request.POST
                customer = CustomerProfile.objects.get(id=cust_id)
                enduser_id =  cust_id +'D' + str(EndUser.objects.count() + 1)
                cp = DeliveryContactPerson.objects.create(id=enduser_id,person_name=data['name'],department_name = data['dept'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],customer_name=customer,created_by=user)
                if cp:
                        context['message'] = 'Successfully registered ' + data['name']
                        context['message_type'] = 'success'
                else:
                        context['message'] = 'Something went wrong'
                        context['message_type'] = 'danger'

                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                receiver = DeliveryContactPerson.objects.filter(customer_name__pk=cust_id)
                context['receiver'] = receiver
                customer = CustomerProfile.objects.get(id=cust_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = cust_id
                context['ContactPersonID'] = contact_person_id
        
                if type == 'CRM':
                        return render(request,"CRM/PO/receiver_selection.html",context)

#Customer PO Process
@login_required(login_url="/employee/login/")
def cpo_process(request, cust_id=None,contact_person_id=None, receiver_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                customer = CustomerProfile.objects.get(id=cust_id)
                customer_contact_person = CustomerContactPerson.objects.get(id=contact_person_id)

                cpo_creation_details = CPOCreationDetail.objects.create(created_by=user)
                
                if receiver_id == 'none':
                        cpo = CustomerPO.objects.create(
                                customer = customer,
                                customer_contact_person = customer_contact_person,
                                cpo_creation_detail = cpo_creation_details
                        )
                else:
                        receiver = DeliveryContactPerson.objects.get(id=receiver_id)
                        cpo = CustomerPO.objects.create(
                                customer = customer,
                                customer_contact_person = customer_contact_person,
                                delivery_contact_person = receiver,
                                cpo_creation_detail = cpo_creation_details
                        )
                print(cpo.id)
                context['cpo_id'] = cpo.id
                return render(request,"CRM/PO/process.html",context)


#Quotation Selection
@login_required(login_url="/employee/login/")
def cpo_create_quotation_selection(request, cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        context['cpo_id'] = cpo_id

        if request.method == 'GET':
                quotation_list = QuotationTracker.objects.all().values(
                        'quotation_no',
                        'customer__name',
                        'customer__location',
                        'quotation_date')
                context['quotation_list'] = quotation_list
                cpo = CustomerPO.objects.get(id=cpo_id)
                customer = cpo.customer
                context['CustomerName'] = customer.name

                if type == 'CRM':
                        return render(request,"CRM/PO/quotation_selection.html",context)

        if request.method == 'POST':
                data = request.POST
                quotations = data['quotation_list'] 
                quotation_list = quotations.split(",")
                
                cpo = CustomerPO.objects.get(id = cpo_id)
                for item in quotation_list:
                        if item != "":
                                quotation = QuotationTracker.objects.get(quotation_no = item)
                                CPOSelectedQuotation.objects.create(
                                        quotation = quotation,
                                        customer_po = cpo
                                )
                #return HttpResponse([{"dd":"ddd"}], content_type='application/json')
                return JsonResponse(data)
                


#Quotation Selection
@login_required(login_url="/employee/login/")
def cpo_quotation_details(request, quotation_no=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                quotation_lineitem = QuotationLineitem.objects.filter(
                        quotation=QuotationTracker.objects.get(quotation_no=quotation_no)
                        ).annotate(
                                basic_value = F('unit_price') + (F('unit_price') * F('margin') / 100)
                        )
                print(quotation_lineitem)
                context['quotation_lineitem'] = quotation_lineitem
                context['quotation_no'] = quotation_no

                if type == 'CRM':
                        return render(request,"CRM/PO/quotation_details.html",context)


#Cpo create lineitem selection
@login_required(login_url="/employee/login/")
def cpo_create_quotation_lineitem_selection(request, cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                context['cpo_id'] = cpo_id
                cpo = CustomerPO.objects.get(id=cpo_id)
                selected_quotation_list = CPOSelectedQuotation.objects.filter(customer_po=cpo)
                i = 1
                for quotation in selected_quotation_list:
                        if i == 1:
                                quotation_lineitems = QuotationLineitem.objects.filter(quotation=quotation.quotation).annotate(
                                        price = F('unit_price') + (F('unit_price') * F('margin') / 100)
                                        ).values(
                                        'id',
                                        'product_title',
                                        'description',
                                        'model',
                                        'brand',
                                        'product_code',
                                        'part_number',
                                        'pack_size',
                                        'hsn_code',
                                        'gst',
                                        'quantity',
                                        'uom',
                                        'price'
                                )
                                i = i + 1 
                        else:
                                quotation_lineitems = quotation_lineitems.union(QuotationLineitem.objects.filter(quotation=quotation.quotation).annotate(
                                        price = F('unit_price') + (F('unit_price') * F('margin') / 100)
                                        ).values(
                                        'id',
                                        'product_title',
                                        'description',
                                        'model',
                                        'brand',
                                        'product_code',
                                        'part_number',
                                        'pack_size',
                                        'hsn_code',
                                        'gst',
                                        'quantity',
                                        'uom',
                                        'price'
                                ))
                
                context['quotation_lineitems'] = quotation_lineitems
                if type == 'CRM':
                        return render(request,"CRM/PO/quotation_product_selection.html",context)

        if request.method == 'POST':
                data = request.POST
                products = data['quotation_product_list'] 
                product_list = products.split(",")
                
                cpo = CustomerPO.objects.get(id = cpo_id)
                for item in product_list:
                        if item != '':
                                try:

                                        quotation_lineitem = QuotationLineitem.objects.get(id = item)

                                        CPOLineitem.objects.create(
                                                cpo = cpo,
                                                quotation_lineitem = quotation_lineitem,
                                                product_title = quotation_lineitem.product_title,
                                                description =  quotation_lineitem.description,
                                                model = quotation_lineitem.model,
                                                brand = quotation_lineitem.brand,
                                                product_code = quotation_lineitem.product_code,
                                                part_no = quotation_lineitem.part_number,
                                                hsn_code = quotation_lineitem.hsn_code,
                                                pack_size = quotation_lineitem.pack_size,
                                                gst = quotation_lineitem.gst,
                                                uom = quotation_lineitem.uom,
                                                quantity = quotation_lineitem.quantity,
                                                unit_price = quotation_lineitem.basic_price,
                                                total_basic_price = quotation_lineitem.total_basic_price,
                                                total_price = quotation_lineitem.total_price,
                                                pending_delivery_quantity = float(quotation_lineitem.quantity),
                                                pending_po_releasing_quantity = float(quotation_lineitem.quantity),
                                        )
                                except Exception as e:
                                        print(e)                      
                #return HttpResponse([{"dd":"ddd"}], content_type='application/json')
                return JsonResponse(data)

#Cpo create lineitem selection
@login_required(login_url="/employee/login/")
def cpo_create_quotation_selection_skip(request, cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                return HttpResponseRedirect(reverse('cpo-create-selected-lineitem',args=[cpo_id]))

#Cpo quotation no search
@login_required(login_url="/employee/login/")
def cpo_quotation_no_search(request):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type

        if request.method == 'GET':
                quotation_lineitem = QuotationLineitem.objects.all()
                context['quotation_lineitem'] = quotation_lineitem
                return render(request,"CRM/PO/quotation_no_search.html",context)


#Cpo create lineitem selection
@login_required(login_url="/employee/login/")
def cpo_create_selected_lineitem(request, cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo = CustomerPO.objects.get(id=cpo_id)
                cpo_lineitem = CPOLineitem.objects.filter(cpo = cpo)
                print(cpo_lineitem)
                context['cpo_lineitem'] = cpo_lineitem

                billing_address = cpo.customer.billing_address
                shipping_address = cpo.customer.shipping_address
                inco_term = cpo.customer.inco_term
                payment_term = cpo.customer.payment_term

                if billing_address == 'Same':
                        context['billing_address'] = cpo.customer.address
                else : 
                        context['billing_address'] = billing_address

                if shipping_address == 'Same':
                        context['shipping_address'] = cpo.customer.address
                else : 
                        context['shipping_address'] = shipping_address

                context['inco_term'] = inco_term
                context['payment_term'] = payment_term

                if type == 'CRM':
                        return render(request,"CRM/PO/quotation_selected_lineitem.html",context)

        if request.method == 'POST':
                data = request.POST
                cpo = CustomerPO.objects.get(id=cpo_id)
                CPOLineitem.objects.create(
                        cpo = cpo,
                        product_title = data['product_title'],
                        description = data['description'],
                        model = data['model'],
                        brand = data['brand'],
                        product_code = data['product_code'],
                        part_no = data['part_no'],
                        pack_size = data['pack_size'],
                        hsn_code = data['hsn_code'],
                        gst = data['gst'],
                        uom = data['uom'],
                        quantity = data['quantity'],
                        unit_price = data['unit_price'],
                        total_basic_price = round((float(data['quantity']) * float(data['unit_price'])),2),
                        total_price = round(((float(data['quantity']) * float(data['unit_price'])) + (float(data['quantity']) * float(data['unit_price']) * float(data['unit_price']) / 100)),2),
                        pending_po_releasing_quantity = data['quantity'],
                        pending_delivery_quantity = data['quantity'],
                )
                return HttpResponseRedirect(reverse('cpo-create-selected-lineitem',args=[cpo_id]))


#Cpo create lineitem edit
@login_required(login_url="/employee/login/")
def cpo_create_lineitem_edit(request, cpo_id=None, lineitem_id = None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo_lineitem = CPOLineitem.objects.get(id = lineitem_id)
                context['cpo_lineitem'] = cpo_lineitem

                if type == 'CRM':
                        return render(request,"CRM/PO/cpo_lineitem_edit.html",context)

        if request.method == 'POST':
                data = request.POST
                total_basic_price = round((float(data['quantity']) * float(data['unit_price'])),2)
                total_price = round((total_basic_price + float(total_basic_price * float(data['gst']) / 100)),2)

                cpo_lineitem = CPOLineitem.objects.get(id=lineitem_id)
                cpo_lineitem.product_title = data['product_title']
                cpo_lineitem.description = data['description']
                cpo_lineitem.model = data['model']
                cpo_lineitem.brand = data['brand']
                cpo_lineitem.product_code = data['product_code']
                cpo_lineitem.part_no = data['part_no']
                cpo_lineitem.pack_size = data['pack_size']
                cpo_lineitem.hsn_code = data['hsn_code']
                cpo_lineitem.gst = data['gst']
                cpo_lineitem.uom = data['uom']
                cpo_lineitem.quantity = data['quantity']
                cpo_lineitem.unit_price = data['unit_price']
                cpo_lineitem.total_basic_price = round(total_basic_price,2)
                cpo_lineitem.total_price = round(total_price,2)
                cpo_lineitem.pending_delivery_quantity = data['quantity']
                cpo_lineitem.pending_po_releasing_quantity = data['quantity']
                cpo_lineitem.save()

                return HttpResponseRedirect(reverse('cpo-create-selected-lineitem',args=[cpo_id]))

#Cpo create lineitem edit
@login_required(login_url="/employee/login/")
def cpo_create_lineitem_delete(request, cpo_id=None, lineitem_id = None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo_lineitem = CPOLineitem.objects.get(id = lineitem_id)
                context['cpo_lineitem'] = cpo_lineitem

                if type == 'CRM':
                        return render(request,"CRM/PO/cpo_lineitem_delete.html",context)

        if request.method == 'POST':
                data = request.POST
                cpo_lineitem = CPOLineitem.objects.get(id=lineitem_id)
                cpo_lineitem.delete()

                return HttpResponseRedirect(reverse('cpo-create-selected-lineitem',args=[cpo_id]))

#Cpo generate
@login_required(login_url="/employee/login/")
def cpo_generate(request, cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                data = request.POST

                cpo = CustomerPO.objects.get(id = cpo_id)

                cpo_lineitem = CPOLineitem.objects.filter(cpo = cpo)

                basic_value = 0
                total_value = 0

                for item in cpo_lineitem:
                        basic_value = basic_value + round(item.total_basic_price,2)
                        total_value = total_value + round(item.total_price,2)                

                cpo.customer_po_no = data['customer_po_no']
                cpo.customer_po_date = data['customer_po_date']
                cpo.billing_address = data['billing_address']
                cpo.shipping_address = data['shipping_address']
                cpo.delivery_date = data['delivery_date']
                cpo.inco_terms = data['inco_terms']
                cpo.payment_terms = data['payment_terms']
                cpo.total_basic_value = round(basic_value,2)
                cpo.total_value = round(total_value,2)
                cpo.po_type = data['po_type']
                
                try:
                        cpo.document1 = request.FILES['supporting_document1']
                except:
                        pass

                try:
                        cpo.document2 = request.FILES['supporting_document2']
                except:
                        pass

                cpo.status = 'Created'

                cpo.save()

                if type == 'CRM':
                        return render(request,"CRM/PO/success.html",context)

#Cpo inprogress list
@login_required(login_url="/employee/login/")
def cpo_creation_inprogress_list(request, cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo_list = CustomerPO.objects.filter(status='creation_inprogress')
                context['cpo_list'] = cpo_list

                if type == 'CRM':
                        return render(request,"CRM/PO/creation_in_progress.html",context)

#Cpo Creation inprogress list
@login_required(login_url="/employee/login/")
def cpo_creation_inprogress_details(request, cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo = CustomerPO.objects.get(id=cpo_id)
                csq_c = CPOSelectedQuotation.objects.filter(customer_po=cpo).count()
                cpol_c = CPOLineitem.objects.filter(cpo=cpo).count()
                
                if cpol_c > 0:
                        return HttpResponseRedirect(reverse('cpo-create-selected-lineitem',args=[cpo_id]))

                if csq_c > 0:
                        return HttpResponseRedirect(reverse('cpo-create-quotation-lineitem-selection',args=[cpo_id]))

                return HttpResponseRedirect(reverse('cpo-create-quotation-selection',args=[cpo_id]))


#CPO Approval List
@login_required(login_url="/employee/login/")
def cpo_approval_list(request):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo_list = CustomerPO.objects.filter(status='Created')
                context['cpo_list'] = cpo_list

                if type == 'Sales':
                        return render(request,"Sales/CPO/approval_list.html",context)

#CPO Approval Lineitem
@login_required(login_url="/employee/login/")
def cpo_approval_lineitem(request,cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo = CustomerPO.objects.get(id=cpo_id)
                cpo_lineitem = CPOLineitem.objects.filter(cpo=cpo)
                context['cpo_lineitem'] = cpo_lineitem
                context['cpo'] = cpo
                users = User.objects.filter(profile__type='Sourcing')
                context['users'] = users

                if type == 'Sales':
                        return render(request,"Sales/CPO/cpo_lineitem.html",context)

#CPO Reject
@login_required(login_url="/employee/login/")
def cpo_reject(request,cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                data = request.POST
                cpo = CustomerPO.objects.get(id=cpo_id)
                cpo.status = 'rejected'
                cpo.rejection_reason = data['rejection']
                cpo.save()
                return HttpResponseRedirect(reverse('cpo-approval-list'))

#CPO Approve
@login_required(login_url="/employee/login/")
def cpo_approve(request,cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                data = request.POST
                assign_user = User.objects.get(username=data['assign1'])

                assign = CPOAssign.objects.create(assign_to=assign_user)

                cpo = CustomerPO.objects.get(id=cpo_id)
                cpo.status = 'approved'
                cpo.cpo_assign_detail = assign
                cpo.save()
                VendorProductSegmentation(cpo_id)
                
                print(data)
                return HttpResponseRedirect(reverse('cpo-approval-list'))

#Mark as Direct Material processing
@login_required(login_url="/employee/login/")
def mark_direct_processing(request,cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                data = request.POST
                assign_user = User.objects.get(username=data['assign1'])

                assign = CPOAssign.objects.create(assign_to=assign_user)
                cpo = CustomerPO.objects.get(id=cpo_id)
                cpo.status = 'direct_processing'
                cpo.cpo_assign_detail = assign
                cpo.save()
                return HttpResponseRedirect(reverse('cpo-approval-list'))

#Vendor Product Segmentation
def VendorProductSegmentation(cpo_id):
        sourcing_list = CPOLineitem.objects.filter(
                cpo=CustomerPO.objects.get(id=cpo_id)
                ).values('quotation_lineitem__sourcing_lineitem__sourcing').distinct()
        print(sourcing_list)
        
        cpo = CustomerPO.objects.get(id=cpo_id)


        #Truncate Process for existing 
        if cpo.segmentation == True:
                return 
        
        for sourcing_id in sourcing_list:

                try:
                
                        print(sourcing_id)

                        sourcing = Sourcing.objects.get(id=sourcing_id['quotation_lineitem__sourcing_lineitem__sourcing'])

                        print(sourcing)

                        vpo = VendorPO.objects.create(
                                cpo = cpo,
                                vendor = sourcing.supplier,
                                vendor_contact_person = sourcing.supplier_contact_person,
                                offer_reference = sourcing.offer_reference,
                                offer_date = sourcing.offer_date,
                                billing_address = 'Aeprocurex Sourcing Private Limited, Shankarappa Complex #4, Hosapalya Main Road, Opposite to Om Shakti Temple, Hosapalya, HSR Layout Extension, Bangalore - 560068',
                                shipping_address = 'Aeprocurex Sourcing Private Limited No 1318, 3rd Floor, 24th Main Rd, Sector 2, HSR Layout, Bengaluru, Karnataka 560102',
                                requester = cpo.cpo_assign_detail.assign_to,
                                payment_term = sourcing.supplier.payment_term,
                                advance_percentage = sourcing.supplier.advance_persentage,
                                di1 = 'Original Invoice & Delivery Challans Four (4) copies each must be submitted at the time of delivery of goods.',
                                di2 = 'Entire Goods must be delivered in Single Lot if not specified otherwise. For any changes, must inform IMMEDIATELY.',
                                di3 = 'Product Specifications, Qty, Price, Delivery Terms are in accordance with your offer # dated: ' + str(sourcing.offer_date),
                                di4 = 'Product Specifications, Qty, Price, Delivery Terms shall remain unchanged for this order.',
                                di5 = 'Notify any delay in shipment as scheduled IMMEDIATELY.',
                                di6 = 'Mail all correspondance to corporate office address only.',
                                di7 = 'Must Submit Warranty Certificate, PO copy, TC copy (if any) and all other documents as per standard documentation'
                                )
                        lineitems = CPOLineitem.objects.filter(quotation_lineitem__sourcing_lineitem__sourcing__supplier=sourcing.supplier, cpo = CustomerPO.objects.get(id = cpo_id))

                        for item in lineitems:
                                unit_price = round(item.quotation_lineitem.sourcing_lineitem.price2,2)
                                total_basic_price = round((unit_price * item.quantity),2)
                                total_price = round((total_basic_price + (total_basic_price * item.gst / 100)),2) 
                                VendorPOLineitems.objects.create(
                                        vpo=vpo,
                                        cpo_lineitem = item,
                                        product_title = item.product_title,
                                        description = item.description,
                                        model = item.model,
                                        brand = item.brand,
                                        product_code = item.product_code,
                                        hsn_code = item.hsn_code,
                                        pack_size = item.pack_size,
                                        gst = item.gst,
                                        uom = item.uom,
                                        quantity = item.quantity,
                                        unit_price = round(unit_price),
                                        actual_price = round(unit_price),
                                        total_basic_price = round(total_basic_price,2),
                                        total_price = round(total_price)
                                )
                                item.segment_status = True
                                item.pending_po_releasing_quantity = 0
                                item.save()
                
                except:
                        pass
        cpo.segmentation = True
        cpo.save()
        DuplicateVPORemover(cpo_id)

#Duplicate VPO Remover
def DuplicateVPORemover(cpo_id):
        cpo = CustomerPO.objects.get(id=cpo_id)
        vpo_counter = VendorPO.objects.filter(cpo=cpo).values('vendor').annotate(c=Count('vendor'))
        print(vpo_counter)
        
        #VPO Counter
        for item in vpo_counter:
                if item['c']>1:
                        print(item['vendor'])
                        vpo_obj = VendorPO.objects.filter(cpo=cpo,vendor = item['vendor'])
                        i = 1
                        for vpo_item in vpo_obj:
                                if i != 1:
                                        vpo_item.delete()
                                i = i + 1


#CPO Rejection List
@login_required(login_url="/employee/login/")
def cpo_rejected_list(request,cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo = CustomerPO.objects.filter(status='rejected')
                context['cpo_list'] = cpo

                if type == 'CRM':
                        return render(request,"CRM/PO/rejected_list.html",context)

#CPO Rejected Lineitem
@login_required(login_url="/employee/login/")
def cpo_rejected_lineitem(request,cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                return HttpResponseRedirect(reverse('cpo-create-selected-lineitem',args=[cpo_id]))

