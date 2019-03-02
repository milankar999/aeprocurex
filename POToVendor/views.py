from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
import io
import random

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins
from rest_framework.renderers import JSONRenderer

from rest_framework.response import Response

from Customer.models import *
from Quotation.models import *
from POFromCustomer.models import *
from Sourcing.models import *
from Supplier.models import *

class PendingCPOList(generics.GenericAPIView,
                                mixins.ListModelMixin
                                ):
        serializer_class = PendingVPOListSerializer
        queryset = CustomerPO.objects.all()
        lookup_field = 'id'

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return CustomerPO.objects.filter(status='approved', cpo_assign_detail__assign_to = self.request.user)

        def get(self,request):
                return self.list(request)


class PendingCPOLineitems(generics.GenericAPIView,
                                mixins.ListModelMixin
                                ):
        serializer_class = PendingCPOLineitemsSerializer
        queryset = CustomerPO.objects.all()
        lookup_field = 'id'

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return CPOLineitem.objects.filter(cpo=CustomerPO.objects.get(id=self.kwargs['id']))

        def get(self,request,id):
                return self.list(request)


# Vendor Product Segmentstion
def VendorProductSegmentation(cpo_id):
        sourcing_list = CPOLineitem.objects.filter(
                cpo=CustomerPO.objects.get(id=cpo_id)
                ).values('quotation_lineitem__sourcing_lineitem__sourcing').distinct()
        print(sourcing_list)
        
        cpo = CustomerPO.objects.get(id=cpo_id)


        #Truncate Process for existing 
        if cpo.segmentation == True:
                return 


        requester = VPORequester.objects.create(requester = cpo.cpo_assign_detail.assign_to)
        
        for sourcing_id in sourcing_list:
                
                print(sourcing_id)

                sourcing = Sourcing.objects.get(id=sourcing_id['quotation_lineitem__sourcing_lineitem__sourcing'])

                print(sourcing)

                vpo = VPO.objects.create(
                        cpo = cpo,
                        vendor = sourcing.supplier,
                        vendor_contact_person = sourcing.supplier_contact_person,
                        offer_reference = sourcing.offer_reference,
                        offer_date = sourcing.offer_date,
                        billing_address = 'Shankarappa Complex #4, Hosapalya Main Road, Opposite to Om Shakti Temple, Hosapalya, HSR Layout Extension, Bangalore - 560068',
                        shipping_address = 'Shankarappa Complex #4, Hosapalya Main Road, Opposite to Om Shakti Temple, Hosapalya, HSR Layout Extension, Bangalore - 560068',
                        requester = requester,
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
                        VPOLineitems.objects.create(
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
                                unit_price = item.unit_price
                        )
                        item.segment_status = True
                        item.save()
        cpo.segmentation = True
        cpo.save()

# Vendor Product Segmentation API
class PendingCPOVendorProductSegmentation(generics.GenericAPIView,
                                mixins.ListModelMixin):
        serializer_class = PendingVPOVendorProductSegmentSerializer
        lookup_field = 'id'

        def get_queryset(self):
                return VPO.objects.filter(cpo=CustomerPO.objects.get(id=self.kwargs['id']))

        def get(self,request,id):
                VendorProductSegmentation(id)
                return self.list(request)

#Segmented Product API
#class PendingCPOSegmentatedProduct(generics.GenericAPIView,
#                                mixins.ListModelMixin):
#        serializer_class = PendingVPOLineitemsSerializer
#        lookup_field = 'id'#
#
#        def get_queryset(self):
#                return VPOLineitems.objects.filter(vpo=VPO.objects.get(id=self.kwargs['vpo_id']))

#        def get(self,request,id,vpo_id):
#                return self.list(request)


#Unassigned PO Lineitems
class PendingCPOUnassignedLineitems(generics.GenericAPIView,
                                mixins.ListModelMixin):
        serializer_class = PendingCPOUnassignedLineitemsSerializer
        lookup_field = 'id'

        def get_queryset(self):
                return CPOLineitem.objects.filter(cpo=CustomerPO.objects.get(id=self.kwargs['id']),segment_status=False)

        def get(self,request,id):
                return self.list(request)

#Edit VPO Lineitem
class VPOLineitemEdit(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin):

        serializer_class = PendingVPOLineitemEditSerializer
        lookup_field = 'id'

        queryset = VPOLineitems.objects.all()

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,cpo_id=None,vpo_id=None,id=None):
                return self.retrieve(request,id)
        
        def put(self,request,cpo_id=None,vpo_id=None,id=None):
                return self.partial_update(request)

        def delete(self,request,cpo_id=None,vpo_id=None,id=None):
                
                vpo_lineitem = VPOLineitems.objects.get(id=id)
                
                cpo_lineitem = vpo_lineitem.cpo_lineitem
                cpo_lineitem.segment_status = False
                cpo_lineitem.save()

                return self.destroy(request,id)

#VPO New Vendor Selection
class VPONewVendorSelection(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin):

        serializer_class = VPONewVendorSelectionSerializer
        lookup_field = 'id'


        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        queryset = SupplierProfile.objects.all()

        def get(self,request,cpo_id=None):
                return self.list(request)

        def post(self,request,cpo_id=None):
                return self.create(request)

        def perform_create(self,serializer):
                supplier_id = 'V9' + str(format(SupplierProfile.objects.count() + 1, '05d'))
                serializer.save(id=supplier_id,created_by=self.request.user)

#VPO COntact Person Selection
class VPONewVendorContactPersonSelection(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin):

        serializer_class = VPOVendorCOntactPersonSelectionSerializer
        lookup_field = 'id'

        queryset = SupplierContactPerson.objects.all()
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return SupplierContactPerson.objects.filter(supplier_name=SupplierProfile.objects.get(id=self.kwargs['id']))

        def get(self,request,cpo_id=None,id = None):
                return self.list(request)

        def post(self,request,cpo_id=None,id = None):
                return self.create(request)

        def perform_create(self,serializer):
                contactperson_id = self.kwargs['id'] +'VP' + str(SupplierContactPerson.objects.count() + 1)
                supplier_name=SupplierProfile.objects.get(id=self.kwargs['id'])
                serializer.save(id=contactperson_id,supplier_name=supplier_name,created_by=self.request.user)

#Generate New VPO
class VPONewVenndorPOSegmentCreation(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin):
        serializer_class = VPONewVenndorPOSegmentCreationSerializer
        lookup_field = 'id'

        queryset = SupplierContactPerson.objects.all()
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self,request,cpo_id=None,vendor_id=None,contact_person_id=None):
                return self.create(request)

        def perform_create(self,serializer):
                serializer.save(
                        cpo = CustomerPO.objects.get(id=self.kwargs['cpo_id']),
                        vendor = SupplierProfile.objects.get(id=self.kwargs['vendor_id']),
                        vendor_contact_person = SupplierContactPerson.objects.get(id=self.kwargs['contact_person_id']),
                        billing_address = 'Shankarappa Complex #4, Hosapalya Main Road, Opposite to Om Shakti Temple, Hosapalya, HSR Layout Extension, Bangalore - 560068',
                        shipping_address = 'Shankarappa Complex #4, Hosapalya Main Road, Opposite to Om Shakti Temple, Hosapalya, HSR Layout Extension, Bangalore - 560068',
                        requester = VPORequester.objects.create(requester=self.request.user),
                        payment_term = SupplierProfile.objects.get(id=self.kwargs['vendor_id']).payment_term,
                        advance_percentage = SupplierProfile.objects.get(id=self.kwargs['vendor_id']).advance_persentage,
                        di1 = 'Original Invoice & Delivery Challans Four (4) copies each must be submitted at the time of delivery of goods.',
                        di2 = 'Entire Goods must be delivered in Single Lot if not specified otherwise. For any changes, must inform IMMEDIATELY.',
                        di3 = 'Product Specifications, Qty, Price, Delivery Terms are in accordance with your offer # ',
                        di4 = 'Product Specifications, Qty, Price, Delivery Terms shall remain unchanged for this order.',
                        di5 = 'Notify any delay in shipment as scheduled IMMEDIATELY.',
                        di6 = 'Mail all correspondance to corporate office address only.',
                        di7 = 'Must Submit Warranty Certificate, PO copy, TC copy (if any) and all other documents as per standard documentation'
                )

#Assign all Unassign Items
class VPOAssignProducts(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None, vpo_id=None):
                
                try :
                        vpo = VPO.objects.get(id=vpo_id)
                        for item_id in request.data['vpo_lineitems']:
                                print(item_id)
                                item = CPOLineitem.objects.get(id=item_id)
                                
                                VPOLineitems.objects.create(
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
                                        unit_price = item.unit_price
                                        )
                                item.segment_status = True
                                item.save()
                        return Response({'Message': 'Success'})
                except:
                        return Response({'Message': 'Error Occured'})

#VPO Basic Info Checking
class VPOBasicInfoChecking(generics.GenericAPIView,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):

        serializer_class = VPOBasicInfoCheckingSerializer
        lookup_field = 'id'

        queryset = VPO.objects.all()

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,cpo_id=None,id=None):
                return self.retrieve(request,id)
        
        def put(self,request,cpo_id=None,id=None):
                return self.partial_update(request)

#VPO Supplier Contact Info Checking
class VPOSupplierCPInfoChecking(generics.GenericAPIView,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        
        serializer_class = VPOSupplierCPInfoCheckingSerializer
        lookup_field = 'id'

        queryset = VPO.objects.all()

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,cpo_id=None,id=None):
                return self.retrieve(request,id)
        
class VPOSCPCURD(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        serializer_class = VPOSCPCURDSerializer
        lookup_field = 'id'

        def get_queryset(self):
                return SupplierContactPerson.objects.filter(supplier_name = VPO.objects.get(id = self.kwargs['vpo_id']).vendor)

        def get(self, request, cpo_id = None, vpo_id = None):
                return self.list(request)

        def post(self, request, cpo_id = None, vpo_id = None):
                return self.create(request)

        def perform_create(self, serializer):
                supplier = VPO.objects.get(id = self.kwargs['vpo_id']).vendor
                serializer.save(
                        id= self.kwargs['vpo_id'] + str(random.randint(1,101)),
                        created_by=self.request.user,
                        supplier_name=supplier)

class VPOSCPEdit(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        serializer_class = VPOSCPCURDSerializer
        lookup_field = 'id'

        queryset = SupplierContactPerson.objects.all()
        
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self, request, cpo_id = None, vpo_id = None, id=None):
                return self.retrieve(request,id)

        def put(self, request, cpo_id = None, vpo_id = None,id = None):
                return self.partial_update(request)


#VPO Supplier Info Checking
class VPOSupplierInfoChecking(generics.GenericAPIView,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        
        serializer_class = VPOSupplierInfoCheckingSerializer
        lookup_field = 'id'

        queryset = VPO.objects.all()

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,cpo_id=None,id=None):
                return self.retrieve(request,id)
        
#VPO Supplier Info Update
class VPOSupplierInfoUpdate(generics.GenericAPIView,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        
        serializer_class = VPOUpdateVendorInfoSerializer
        lookup_field = 'id'

        queryset = SupplierProfile.objects.all()

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,cpo_id=None,vpo_id=None,id=None):
                return self.retrieve(request,id)

        def put(self,request,cpo_id=None,vpo_id=None,id=None):
                return self.update(request,id)

#VPO Receiver Info Checking
class VPOReceiverInfoChecking(generics.GenericAPIView,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        serializer_class = VPOReceiverSerilizer
        lookup_field = 'id'

        queryset = VPO.objects.all()

        def get(self,request,cpo_id=None,id=None):
                return self.retrieve(request,id)

        def put(self,request,cpo_id=None,id=None):
                return self.partial_update(request)

#VPO Terms and Conditions
class VPOTermsConditions(generics.GenericAPIView,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        serializer_class = VPOTermsConditionsSerializer
        lookup_field = 'id'

        queryset = VPO.objects.all()

        def get(self,request,cpo_id=None,id=None):
                return self.retrieve(request,id)

        def put(self,request,cpo_id=None,id=None):
                return self.partial_update(request)

 
#VPO Delivery Instructions
class VPODeliveryInstructions(generics.GenericAPIView,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        serializer_class = VPODISerializer
        lookup_field = 'id'

        queryset = VPO.objects.all()

        def get(self,request,cpo_id=None,id=None):
                return self.retrieve(request,id)

        def put(self,request,cpo_id=None,id=None):
                return self.partial_update(request)

#VPO Launch
class VPOLaunch(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None, vpo_id=None):
                try :
                        vpo = VPO.objects.get(id=vpo_id)
                        vpo_lineitem = VPOLineitems.objects.filter(vpo=vpo)

                        

                        if vpo.offer_reference == '':
                                return Response({'Message': 'Offer Reference Not Found'})

                        if vpo.offer_date == '':
                                return Response({'Message': 'Undefined Offer Date Found'})

                        if vpo.delivery_date == '':
                                return Response({'Message': 'Delivery Date Not Found'})

                        if vpo.billing_address == '':
                                return Response({'Message': 'Billing Addresss Not Found'})

                        if vpo.payment_term == 0 and vpo.advance_percentage == 0:
                                return Response({'Message': 'Payment Terms and Advance Percentage are not Clear'})

                        if vpo.inco_terms == 0:
                                return Response({'Message': 'Inco Terms Not Found'})



                        for item in vpo_lineitem:
                                if item.product_title == '':
                                        return Response({'Message': 'Undefined Product Title Found'})
                                
                                if item.description == '':
                                        return Response({'Message': 'Undefined Product Description Found'})

                                if item.gst == '':
                                        return Response({'Message': 'Undefined GST Found'})

                                if item.uom == '':
                                        return Response({'Message': 'Undefined UOM Found'})

                                if item.quantity == '':
                                        return Response({'Message': 'Undefined Quantity Found'})

                                if item.unit_price == '':
                                        return Response({'Message': 'Undefined Unit Price Found'})
                                
                        vpo.status = 'Requested'
                        vpo.save()
                        return Response({'Message': 'Success'})
                except:
                        return Response({'Message': 'Error Occured'})

#VPO Preview
class VPOPreview(generics.GenericAPIView,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin):
        
        serializer_class = VPOPreviewSerializer
        lookup_field = 'id'

        queryset = VPO.objects.all() 

        def get(self,request,cpo_id=None, id=None):
                return self.retrieve(request,id)
