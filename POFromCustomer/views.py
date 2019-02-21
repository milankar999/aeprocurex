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