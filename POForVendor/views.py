from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from rest_framework import viewsets
from django.http import Http404, HttpResponse, JsonResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
from .serializers import *
from django.db.models import F
import io
import random
import datetime


from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from rest_framework.response import Response

from Customer.models import *
from Quotation.models import *
from POFromCustomer.models import *
from Sourcing.models import *
from Supplier.models import *
from django.db.models import Q
from django.db.models import Count

from django.db.models import F
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import Image, Paragraph, Table, TableStyle
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
import textwrap
from django.views.static import serve
from django.http import FileResponse
#from datetime import datetime
from num2words import num2words

#Pending CPO List
class PendingCPOList(generics.GenericAPIView,
                                mixins.ListModelMixin
                                ):
        serializer_class = PendingCPOListSerializer
        queryset = CustomerPO.objects.all()
        lookup_field = 'id'

        #Check Authentications
        authentication_classes=[TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return CustomerPO.objects.filter(status='approved', cpo_assign_detail__assign_to = self.request.user)

        def get(self,request):
                return self.list(request)

#Pending CPO Lineitems
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


#Mark CPO as PO Relesing Completed
class PendingCPOMarkCompleted(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None):
                #if 1<2:
                try :
                        cpo = CustomerPO.objects.get(id=cpo_id)
                        vpo_list = VendorPO.objects.filter(cpo=cpo)

                        for vpo in vpo_list:
                                if vpo.po_status == 'Preparing' or vpo.po_status == 'Rejected':     
                                        return Response({'Message': 'Found Some Vendor PO Still pending'})

                        cpo_lineitem = CPOLineitem.objects.filter(cpo=cpo)
                        
                        for item in cpo_lineitem:
                                if item.segment_status == False:
                                        return Response({'Message': 'Some Customer PO Lineitem found Still pending'})

                        cpo.status = 'po_processed'
                        cpo.save()
                        return Response({'Message': 'Success'})

                except:
                        return Response({'Message': 'Error Occured'})


# Vendor Product Segmentation API
class PendingCPOVendorProductSegmentation(generics.GenericAPIView,
                                mixins.ListModelMixin):
        serializer_class = PendingVPOVendorProductSegmentSerializer
        lookup_field = 'id'

        def get_queryset(self):
                return VendorPO.objects.filter(Q(cpo=CustomerPO.objects.get(id=self.kwargs['id']), po_status = 'Preparing') | Q(cpo=CustomerPO.objects.get(id=self.kwargs['id']), po_status = 'Rejected'))

        def get(self,request,id):
                VendorProductSegmentation(id)
                return self.list(request)

#Unassigned PO Lineitems
class PendingCPOUnassignedLineitems(generics.GenericAPIView,
                                mixins.ListModelMixin):
        serializer_class = PendingCPOUnassignedLineitemsSerializer
        lookup_field = 'id'

        def get_queryset(self):
                return CPOLineitem.objects.filter(cpo=CustomerPO.objects.get(id=self.kwargs['id']),segment_status=False)

        def get(self,request,id):
                return self.list(request)

#Remove 
class VPORemove(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None, vpo_id = None):
                #if 1<2:
                try :
                        cpo = CustomerPO.objects.get(id=cpo_id)
                        vpo = VendorPO.objects.get(id=vpo_id)

                        vpo_lineitem = VendorPOLineitems.objects.filter(vpo=vpo)

                        for item in vpo_lineitem:
                                item.cpo_lineitem.segment_status = False
                                item.cpo_lineitem.save()

                        vpo.delete()
                        return Response({'Message': 'Success'})

                except:
                        return Response({'Message': 'Error Occured'})




#Edit VPO Lineitem
class VPOLineitemEdit(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin):

        serializer_class = PendingVPOLineitemEditSerializer
        lookup_field = 'id'

        queryset = VendorPOLineitems.objects.all()

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,cpo_id=None,vpo_id=None,id=None):
                return self.retrieve(request,id)
        
        def put(self,request,cpo_id=None,vpo_id=None,id=None):
                return self.partial_update(request)

        def perform_update(self, serializer):
                serializer.save()
                vpo_lineitem = VendorPOLineitems.objects.get(id = self.kwargs['id'])
                vpo_lineitem.actual_price = round((vpo_lineitem.unit_price - (vpo_lineitem.unit_price * vpo_lineitem.discount / 100)),2)
                vpo_lineitem.total_basic_price = round((vpo_lineitem.actual_price * vpo_lineitem.quantity),2)
                vpo_lineitem.total_price = round((vpo_lineitem.total_basic_price + (vpo_lineitem.total_basic_price * vpo_lineitem.gst / 100)),2)
                vpo_lineitem.save()
                
                

        def delete(self,request,cpo_id=None,vpo_id=None,id=None):
                
                vpo_lineitem = VendorPOLineitems.objects.get(id=id)
                
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

#VPO Contact Person Selection
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
                        billing_address = 'Aeprocurex Sourcing Private Limited, Shankarappa Complex #4, Hosapalya Main Road, Opposite to Om Shakti Temple, Hosapalya, HSR Layout Extension, Bangalore - 560068',
                        shipping_address = 'Aeprocurex Sourcing Private Limited,No 1318, 3rd Floor, 24th Main Rd, Sector 2, HSR Layout, Bengaluru, Karnataka 560102',
                        requester = self.request.user,
                        di1 = 'Original Invoice & Delivery Challans Four (4) copies each must be submitted at the time of delivery of goods.',
                        di2 = 'Entire Goods must be delivered in Single Lot if not specified otherwise. For any changes, must inform IMMEDIATELY.',
                        di3 = 'Product Specifications, Qty, Price, Delivery Terms are in accordance with your offer # ',
                        di4 = 'Product Specifications, Qty, Price, Delivery Terms shall remain unchanged for this order.',
                        di5 = 'Notify any delay in shipment as scheduled IMMEDIATELY.',
                        di6 = 'Mail all correspondance to corporate office address only.',
                        di7 = 'Must Submit Warranty Certificate, PO copy, TC copy (if any) and all other documents as per standard documentation'
                )

#Assign  Unassign Items
class VPOAssignProducts(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None, vpo_id=None):
                #if 1<2:
                try :
                        vpo = VendorPO.objects.get(id=vpo_id)
                        for item_id in request.data['vpo_lineitems']:
                                print(item_id)
                                item = CPOLineitem.objects.get(id=item_id)
                                
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
                                        unit_price = 0                                        
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

        queryset = VendorPO.objects.all()

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

        queryset = VendorPO.objects.all()

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self,request,cpo_id=None,id=None):
                return self.retrieve(request,id)

#VPO Edit
class VPOSCPEdit(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        serializer_class = VPOSCPEditSerializer
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

        queryset = VendorPO.objects.all()

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
                return self.partial_update(request,id)

#VPO Receiver Info Checking
class VPOReceiverInfoChecking(generics.GenericAPIView,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin):
        
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        serializer_class = VPOReceiverSerilizer
        lookup_field = 'id'

        queryset = VendorPO.objects.all()

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

        queryset = VendorPO.objects.all()

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

        queryset = VendorPO.objects.all()

        def get(self,request,cpo_id=None,id=None):
                return self.retrieve(request,id)

        def put(self,request,cpo_id=None,id=None):
                return self.partial_update(request)

##Get Financial Year
#function take input of the datestring like 2017-05-01
def get_financial_year(datestring):
        date = datetime.datetime.strptime(datestring, "%Y-%m-%d").date()
        #initialize the current year
        year_of_date=date.year
        #initialize the current financial year start date
        financial_year_start_date = datetime.datetime.strptime(str(year_of_date)+"-04-01","%Y-%m-%d").date()
        if date<financial_year_start_date:
                return str(financial_year_start_date.year-1)[2:4] + str(financial_year_start_date.year)[2:4]
        else:
                return str(financial_year_start_date.year)[2:4] + str(financial_year_start_date.year+1)[2:4]

#VPO Launch
class VPOLaunch(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None, vpo_id=None):
                #if 1<2:
                try :
                        vpo = VendorPO.objects.get(id=vpo_id)
                        vpo_lineitem = VendorPOLineitems.objects.filter(vpo=vpo)

                        
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



                        basic_value = 0
                        total_value = 0
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
                        
                                basic_value = round((basic_value + item.total_basic_price),2)
                                total_value = round((total_value + item.total_price),2)
                        
                        all_total_value = total_value

                        try:
                                all_total_value = all_total_value + vpo.freight_charges
                        except:
                                pass

                        try:
                                all_total_value = all_total_value + vpo.custom_duties
                        except:
                                pass

                        try:
                                all_total_value = all_total_value + vpo.pf
                        except:
                                pass

                        try:
                                all_total_value = all_total_value + vpo.insurance
                        except:
                                pass

                        print(vpo.po_status)        
                        if vpo.po_status == 'Preparing': 
                                vpo_count = VendorPOTracker.objects.count() + 1
                                requester_name = VendorPO.objects.get(id=vpo_id).requester.first_name
                                po_number = 'ASPL-' + requester_name[0] + '-' + get_financial_year(datetime.datetime.today().strftime('%Y-%m-%d')) + "{:04d}".format(vpo_count)
                                print(po_number)
                                VendorPOTracker.objects.create(
                                        po_number = po_number,
                                        vpo = vpo,
                                        requester = self.request.user,
                                        basic_value = basic_value,
                                        total_value = total_value,
                                        all_total_value = all_total_value)
                                vpo.po_status = 'Requested'
                                vpo.save()
                                return Response({'Message': 'Success'})

                        if vpo.po_status == 'Rejected':
                                vpo_tracker = VendorPOTracker.objects.get(vpo = vpo)
                                vpo_tracker.status = 'Requested'
                                vpo_tracker.basic_value = basic_value
                                vpo_tracker.total_value = total_value
                                vpo_tracker.all_total_value = all_total_value
                                vpo_tracker.save()
                                
                                vpo.po_status = 'Requested'
                                vpo.vpo_type = 'Regular'
                                vpo.save()
                                return Response({'Message': 'Success'})

                except:
                        return Response({'Message': 'Error Occured'})

#Mark as Cash Purchase
class VPOLaunchDirectPurchase(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, cpo_id = None, vpo_id=None):
                #if 1<2:
                try :
                        vpo = VendorPO.objects.get(id=vpo_id)
                        print(vpo)
                        vpo_lineitem = VendorPOLineitems.objects.filter(vpo=vpo)

                        if vpo.payment_term == 0 and vpo.advance_percentage == 0:
                                return Response({'Message': 'Payment Terms and Advance Percentage are not Clear'})

                        basic_value = 0
                        total_value = 0

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

                                basic_value = round((basic_value + item.total_basic_price),2)
                                total_value = round((total_value + item.total_price),2)

                        print(basic_value)
                        print(total_value)
                        all_total_value = total_value

                        try:
                                all_total_value = all_total_value + vpo.freight_charges
                        except:
                                pass

                        try:
                                all_total_value = all_total_value + vpo.custom_duties
                        except:
                                pass

                        try:
                                all_total_value = all_total_value + vpo.pf
                        except:
                                pass

                        try:
                                all_total_value = all_total_value + vpo.insurance
                        except:
                                pass



                        print(vpo.po_status)        
                        if vpo.po_status == 'Preparing': 
                                vpo_count = VendorPOTracker.objects.count() + 1
                                requester_name = VendorPO.objects.get(id=vpo_id).requester.first_name
                                po_number = 'ASPL-' + requester_name[0] + '-' + get_financial_year(datetime.datetime.today().strftime('%Y-%m-%d')) + "{:04d}".format(vpo_count)
                                print(po_number)
                                VendorPOTracker.objects.create(
                                        po_number = po_number,
                                        vpo = vpo,
                                        vpo_type = 'Direct Buying',
                                        requester = self.request.user,
                                        basic_value = basic_value,
                                        total_value = total_value,
                                        all_total_value = all_total_value)
                                vpo.po_status = 'Requested'

                                vpo.save()
                                return Response({'Message': 'Success'})

                        if vpo.po_status == 'Rejected':
                                vpo_tracker = VendorPOTracker.objects.get(vpo = vpo)
                                vpo_tracker.status = 'Requested'
                                vpo_tracker.basic_value = basic_value
                                vpo_tracker.total_value = total_value
                                vpo_tracker.all_total_value = all_total_value
                                vpo_tracker.save()

                                vpo.po_status = 'Requested'
                                vpo.vpo_type = 'Direct Buying'
                                vpo.save()
                                return Response({'Message': 'Success'})

                except:
                        return Response({'Message': 'Error Occured'})


#VPO Preview
class VPOPreview(APIView):
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self, request, format=None, cpo_id = None, vpo_id = None):
                vpo = VendorPO.objects.filter(id = vpo_id).values(
                        'vendor__name',
                        'vendor__state',
                        'vendor__payment_term',
                        'vendor_contact_person__name',
                        'vendor__location',
                        'vendor__address',
                        'vendor__gst_number',
                        'offer_reference',
                        'offer_date',
                        'billing_address',
                        'shipping_address',
                        'delivery_date',
                        'custom_duties',
                        'pf',
                        'freight_charges',
                        'insurance',
                        'mode_of_transport',
                        'inco_terms',
                        'installation',
                        'comments',
                        'di1',
                        'di2',
                        'di3',
                        'di4',
                        'di5',
                        'di6',
                        'di7',
                        'di8',
                        'di9',
                        'di10',
                )
                return Response(vpo)  

#VPO Preview Lineitem
class VPOPreviewLineitems(generics.GenericAPIView,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin):
        
        serializer_class = VPOPreviewLineitemsSerializer
        lookup_field = 'id'
        
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return VendorPOLineitems.objects.filter(vpo=VendorPO.objects.get(id=self.kwargs['id']))

        def get(self, request, cpo_id = None, id=None):
                return self.list(request)

#VPO Approval List
class VPOApprovalList(APIView):
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self, request, format=None):
                vpo = VendorPOTracker.objects.filter(status = 'Requested').values(
                        'po_number',
                        'po_date',
                        'vpo__id',
                        'vpo__vendor__name',
                        'vpo__vendor_contact_person__name',
                        'vpo__vendor__location'
                )
                return Response(vpo)

#VPO Pending Approval List
@login_required(login_url="/employee/login/")
def VPOPendingApprovalList(request):
        context={}
        context['PO'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == 'GET':
                vpo = VendorPOTracker.objects.filter(status = 'Requested')
                context['vpo'] = vpo

                if type == 'Sales':
                        return render(request,"Sales/VPO/approval_list.html",context)


#VPO Regular Pending Approval List
@login_required(login_url="/employee/login/")
def VPOPendingApprovalLineitems(request,po_number=None):
        context={}
        context['PO'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == 'GET':
                vpo = VendorPOTracker.objects.get(po_number=po_number)
                vpo_lineitem = VendorPOLineitems.objects.filter(vpo=vpo.vpo)
                context['vpo'] = vpo
                context['vpo_lineitem'] = vpo_lineitem
                PO_Generator(po_number)

                if type == 'Sales':
                        return render(request,"Sales/VPO/vpo_lineitem.html",context)

#VPO Regular Pending Approval Get Copy
@login_required(login_url="/employee/login/")
def VPOPendingApprovalGetCopy(request,po_number=None):
        context={}
        context['PO'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == 'GET':
                PO_Generator(po_number)
                return FileResponse('/api/media/po/'+po_number+'.pdf', as_attachment=True, filename= po_number + '.pdf')


#VPO Approve
@login_required(login_url="/employee/login/")
def VPOApprove(request,po_number=None):
        context={}
        context['PO'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == 'POST':
                vpo_tracker = VendorPOTracker.objects.get(po_number=po_number)
                vpo_tracker.status = 'Approved' 
                vpo_tracker.vpo.po_status = 'Approved'
                vpo_tracker.vpo.save()
                vpo_tracker.save()

                if type == 'Sales':
                        return HttpResponseRedirect(reverse('vpo-pending-approval-list'))

#VPO Reject
@login_required(login_url="/employee/login/")
def VPOReject(request,po_number=None):
        context={}
        context['PO'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == 'POST':
                vpo_tracker = VendorPOTracker.objects.get(po_number=po_number)
                vpo_tracker.status = 'Rejected' 
                vpo_tracker.vpo.po_status = 'Rejected'
                vpo_tracker.vpo.save()
                vpo_tracker.save()

                if type == 'Sales':
                        return HttpResponseRedirect(reverse('vpo-pending-approval-list'))

#VPO Lineitems
class VPOApprovalLineitems(generics.GenericAPIView,
                                mixins.ListModelMixin):
        serializer_class = VPOApprovalLineitemsSerializer
        lookup_field = 'po_number'
        
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return VendorPOLineitems.objects.filter(vpo=VendorPOTracker.objects.get(po_number = self.kwargs['po_number']).vpo)

        def get(self, request, id = None, po_number=None):
                print(VendorPOLineitems.objects.filter(vpo = VendorPOTracker.objects.get(po_number = self.kwargs['po_number']).vpo))
                return self.list(request)

#VPO Approval Informations
class VPOApprovalInfo(generics.GenericAPIView,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin):
        serializer_class = VPOApprovalInfoSerializer
        lookup_field = 'id'
        
        queryset = VendorPO.objects.all() 
        
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self, request, id = None, po_number=None):
                return self.retrieve(request, id)

#VPO Approval Preview
class VPOApprovalPreview(APIView):
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self, request, format=None, vpo_id = None, po_number = None):
                vpo = VendorPOTracker.objects.filter(po_number = po_number).values(
                        'po_number',
                        'po_date',
                        'vpo__id',
                        'vpo__vendor__name',
                        'vpo__vendor__state',
                        'vpo__vendor__payment_term',
                        'vpo__vendor_contact_person__name',
                        'vpo__vendor__location',
                        'vpo__vendor__address',
                        'vpo__vendor__gst_number',
                        'vpo__offer_reference',
                        'vpo__offer_date',
                        'vpo__billing_address',
                        'vpo__shipping_address',
                        'vpo__delivery_date',
                        'vpo__custom_duties',
                        'vpo__freight_charges',
                        'vpo__pf',
                        'vpo__insurance',
                        'vpo__mode_of_transport',
                        'vpo__inco_terms',
                        'vpo__installation',
                        'vpo__comments',
                        'vpo__di1',
                        'vpo__di2',
                        'vpo__di3',
                        'vpo__di4',
                        'vpo__di5',
                        'vpo__di6',
                        'vpo__di7',
                        'vpo__di8',
                        'vpo__di9',
                        'vpo__di10',
                )
                return Response(vpo)  

#VPO Approve
#class VPOApprove(APIView):
#        parser_classes = (JSONParser,)

        #Check Authentications
#        authentication_classes = [TokenAuthentication, SessionAuthentication]
#        permission_classes = [IsAuthenticated,]

#        def post(self, request, format=None, vpo_id = None, po_number=None):    
                                          
#                try:
#                        vpo = VPO.objects.get(id = vpo_id)
#                        vpo_tracker = VPOTracker.objects.get(po_number=po_number)

#                        vpo.po_status = 'Approved'
#                        vpo_tracker.status = 'Approved' 

#                        vpo.save()
#                        vpo_tracker.save()

#                        return Response({'Message': 'Success'})                      
#                except:
#                        return Response({'Message': 'Error Occured'})

#VPO Reject
#class VPOReject(APIView):
#        parser_classes = (JSONParser,)

        #Check Authentications
#        authentication_classes = [TokenAuthentication, SessionAuthentication]
#        permission_classes = [IsAuthenticated,]

#        def post(self, request, format=None, po_number=None):            
#                try:
#                        vpo = VPO.objects.get(id = vpo_id)
#                        vpo_tracker = VPOTracker.objects.get(po_number=po_number)#

#                        vpo.po_status = 'Rejected'
#                        vpo_tracker.status = 'Rejected' 

#                        vpo.save()
#                        vpo_tracker.save()

#                        return Response({'Message': 'Success'})                      
#                except:
#                        return Response({'Message': 'Error Occured'})

#VPO Ready List
class VPOReadyList(APIView):
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self, request, format=None):
                vpo = VendorPOTracker.objects.filter(status = 'Approved', vpo__requester = self.request.user).values(
                        'po_number',
                        'po_date',
                        'vpo__id',
                        'vpo__vendor__name',
                        'vpo__vendor_contact_person__name',
                        'vpo__vendor__location'
                )
                return Response(vpo)        

#VPO Ready details
class VPOReadyPreview(generics.GenericAPIView,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin):
        serializer_class = VPOApprovalLineitemsSerializer
        lookup_field = 'po_number'
        
        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get_queryset(self):
                return VendorPOLineitems.objects.filter(vpo=VendorPOTracker.objects.get(po_number = self.kwargs['po_number']).vpo)

        def get(self, request, id = None, po_number=None):
                print(VendorPOLineitems.objects.filter(vpo = VendorPOTracker.objects.get(po_number = self.kwargs['po_number']).vpo))
                return self.list(request)

#VPO Ready Change Info
class VPOReadyChangeInfo(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def post(self, request, format=None, po_number=None):            
                try:
                        vpo_tracker_obj = VPOTracker.objects.get(po_number=po_number)
                        vpo_obj = vpo_tracker_obj.vpo

                        vpo_obj.po_status = 'Rejected'
                        vpo_tracker_obj.status = 'Rejected'

                        vpo_tracker_obj.save()
                        vpo_obj.save()

                        return Response({'Message': 'Success'})

                except :
                        return Response({'Message': 'Error Occured'})

#Add Front Page Header
def Add_Header(pdf):
        pdf.drawInlineImage("static/image/aeprocurex.jpg",360,750,220,70)
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawString(10,763,"AEPROCUREX SOURCING PRIVATE LIMITED")

        pdf.setFont('Helvetica',9)
        #pdf.setFillColor(HexColor('#000000'))
        pdf.drawString(10,752,"Regd. Office: Shankarappa Complex, No.4")
        pdf.drawString(10,741,"Hosapalya Main Road, Opp. To Om Shakti Temple")
        pdf.drawString(10,730,"HSR Layout Extension,Bangalore - 560068")

        pdf.drawString(10,719,"Telephone: 080-43743314, +91 9964892600")
        pdf.drawString(10,708,"E-mail: sales.p@aeprocurex.com")
        pdf.drawString(10,697,"GST No. 29AAQCA2809L1Z6")
        pdf.drawString(10,686,"PAN No. - AAQCA2809L")
        pdf.drawString(10,675,"CIN No.-U74999KA2017PTC108349")

        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawString(300,700,"PURCHASE ORDER")
        #pdf.setFillColor(yellow)
        pdf.rect(300,696,275,1, stroke=1, fill=1)

#Add Footer 
def Add_Footer(pdf):
    pdf.setFont('Helvetica', 10)
    pdf.drawString(200,15,'THANK YOU FOR YOUR BUSINESS')
    pdf.drawString(520,15,'Page-No : ' + str(pdf.getPageNumber()))

#Add Po Information
def po_information(pdf,po_no,po_date,delivery_date,offer_reference,offer_date,vendor_code):
        if vendor_code == None:
                vendor_code = ' '

        pdf.setFont('Helvetica', 9)
        pdf.drawString(300,680,"Order No :")
        pdf.drawString(300,667,"Order Date :")
        pdf.drawString(300,654,"Delivery Date :")
        pdf.drawString(300,635,"Offer Reference :")
        pdf.drawString(300,622,"Offer Date :")
        pdf.drawString(300,610,"Vendor Code :")

        pdf.setFont('Helvetica-Bold', 9)
        try:
                pdf.drawString(390,680,po_no)
        except:
                pdf.drawString(390,680,"")
        try:
                pdf.drawString(390,667,str(po_date.strftime('%d, %b %Y')))
        except:
                pdf.drawString(390,667,"")
        try:
                pdf.drawString(390,654,str(delivery_date.strftime('%d, %b %Y')))
        except:
                pdf.drawString(390,654,"")
        try:
                pdf.drawString(390,635,offer_reference)
        except:
                pdf.drawString(390,635,"")
        try:
                pdf.drawString(390,622,str(offer_date.strftime('%d, %b %Y')))
        except:
                pdf.drawString(390,622,"")
        try:
                pdf.drawString(390,610,vendor_code)
        except:
                pdf.drawString(390,610,"")

#Add PO To
def Add_To(pdf,supplier_name,address,gst,shipping_address,billing_address):
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawString(10,622,'PURCHASE ORDER TO')
        pdf.rect(10,618,145,0.5, stroke=1, fill=1)
        #pdf.setFont('Helvetica-Bold', 13)

        pdf.setFont('Helvetica-Bold', 10)
        pdf.drawString(10,605,supplier_name)
        pdf.setFont('Helvetica', 10)
    
        wrapper = textwrap.TextWrapper(width=115) 
        word_list = wrapper.wrap(text=address)
        y = 590 
        for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 13
        y = y -3
        try:
                pdf.drawString(10,y,'GST # :' + gst)
                y = y - 13
        except:
                pass
        y = y - 3

        pdf.setFont('Helvetica-Bold', 10)
        pdf.setFillColor(HexColor('#000000'))
        pdf.drawString(10,y,'Billing Address')
        y = y - 11
        wrapper = textwrap.TextWrapper(width=140)
        word_list = wrapper.wrap(text=billing_address)
        pdf.setFont('Helvetica', 9)
        for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 11

        y = y - 3

        pdf.setFont('Helvetica-Bold', 10)
        pdf.setFillColor(HexColor('#000000'))
        pdf.drawString(10,y,'Material Delivery Address')
        y = y - 11
        word_list = wrapper.wrap(text=shipping_address)
        pdf.setFont('Helvetica', 9)
        for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 11
        return(y)

def Add_Receiver(pdf,y,receiver_name,phone1,phone2,dept):
        try:
                receiver_info = receiver_name
        except:
                pass
        try:
                if phone1 != '':
                        receiver_info = receiver_info + ' ,Phone No - ' + phone1
        except:
                pass
        try:
                if phone2 != '':
                        receiver_info = receiver_info + ' / ' + phone2
        except:
                pass
        try:
                if dept != '':
                        receiver_info = receiver_info + ' ,Dept : ' + dept
        except:
                pass
        try:
                pdf.setFont('Helvetica-Bold', 6)
                pdf.drawString(10,y,"Material Receiver - " + receiver_info)
                y = y - 10
        except:
                pass
        return(y)

#ADD Kind Attention Inf
def Add_grt(pdf,y,contact_person):
        #pdf.rect(10,y + 5,570,0.5, stroke=1, fill=1)
        y = y - 8
        pdf.setFont('Helvetica-Bold', 9)
        pdf.drawString(10,y,"Kind Attention " + contact_person)
        y = y - 10
        pdf.setFont('Helvetica', 8)
        pdf.drawString(10,y,"Dear Sir / Madam,")
        y = y - 9
        pdf.drawString(10,y,"Please supply the under noted goods subject to the instructions herein below and terms and conditions set out overleaf. All supplies must be effected at our site")
        y = y - 9
        pdf.drawString(10,y,"address as mentioned below. If nothing contrary is heard within 48 hours of the receipt to this order, it will be understood that the order has been accepted in full.")
        y = y - 9
        pdf.drawString(10,y,"Our Order No.& date should be mentioned clearly in your challan(s) and invoice(s).")
        y = y - 9
        return(y)

#Add Table Header
def Add_Table_Header(pdf,y):
        pdf.rect(10,y,570,1, stroke=1, fill=1)
        pdf.setFillColor(HexColor('#E4E4E4'))
        pdf.rect(10,y-31,570,30, stroke=0, fill=1)
        #Colum headers
        pdf.setFillColor(HexColor('#000000'))
        pdf.setFont('Helvetica-Bold', 8)
        pdf.drawString(12,y-17,'SL #')
        pdf.drawString(60,y-17,'Material / Description / Specification')
        pdf.drawString(230,y-17,'Quantity')
        pdf.drawString(283,y-17,'UOM')
        pdf.drawString(330,y-11,'Initial Basic Price')
        pdf.drawString(336,y-22,'/ UOM (IN INR)')
        pdf.drawString(420,y-11,'Discount')
        pdf.drawString(430,y-22,'(%)')
        pdf.drawString(480,y-11,'Final Basic Price')
        pdf.drawString(482,y-22,' / UOM (IN INR)')
        y = y - 31
        pdf.rect(10,y,570,0.1, stroke=1, fill=1)
        y = y - 10
        return(y)

#Add New Page
def add_new_page(pdf,po_number):
        pdf.showPage()
        pdf.drawInlineImage("static/image/aeprocurex.jpg",360,750,220,70)
        Add_Footer(pdf)
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawString(10,763,'ORDER NO : ' + po_number)
        pdf.line(10,748,580,748)
        return(740)

#Add Lineitem
def add_lineitem(pdf,y,i,po_number,product_title,description,model,brand,product_code,hsn_code,gst,quantity,uom,unit_price,discount,discounted_price,total_discounted_price,gst_value,total_value):
        
        pdf.setFont('Helvetica', 9)
        pdf.drawString(12,y,str(i))
        pdf.drawString(230,y,str(quantity))
        pdf.drawString(283,y,uom.upper())
        pdf.drawString(330,y,unit_price)
        pdf.drawString(420,y,discount) 
        pdf.drawString(480,y,discounted_price)

        #Product title
        material_wrapper = textwrap.TextWrapper(width=45)
        title_word_list = material_wrapper.wrap(text=product_title)
    
        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                y = Add_Table_Header(pdf,y)
                pdf.setFont('Helvetica', 9)

        for element in title_word_list:
                pdf.drawString(40,y,element)
                y = y - 11
        
        
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)
                        y = Add_Table_Header(pdf,y)
                        pdf.setFont('Helvetica', 9)
        
        y = y + 10
        
        #Description
        description_word_list = material_wrapper.wrap(description)
        for element in description_word_list:
                pdf.drawString(40,y-10,element)
                y = y - 11
    
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)
                        y = Add_Table_Header(pdf,y)
                        pdf.setFont('Helvetica', 9)
        y=y-3
        #Make
        if brand != '':
                try:
                        brand_word_list = material_wrapper.wrap('Make :' + brand)
                        for element in brand_word_list:
                
                                pdf.drawString(40,y-10,element)
                                y = y - 11

                                #Page Break
                                if y < 50:
                                        y = add_new_page(pdf,po_number)
                                        y = Add_Table_Header(pdf,y)
                                        pdf.setFont('Helvetica', 9)
                                
                        y=y-3
                except:
                        pass

        #Model
        if model != '':
                try:
                        model_word_list = material_wrapper.wrap('Model :' + model)
                        for element in model_word_list:
                
                                pdf.drawString(40,y-10,element)
                                y = y - 11

                                #Page Break
                                if y < 50:
                                        y = add_new_page(pdf,po_number)
                                        y = Add_Table_Header(pdf,y)
                                        pdf.setFont('Helvetica', 9)
                                
                        y=y-3
                except:
                        pass

        #Product Code
        if product_code != '':
                try:
                        product_code_word_list = material_wrapper.wrap('Product Code :' + product_code)
                        for element in product_code_word_list:
                
                                pdf.drawString(40,y-10,element)
                                y = y - 11

                                #Page Break
                                if y < 50:
                                        y = add_new_page(pdf,po_number)
                                        y = Add_Table_Header(pdf,y)
                                        pdf.setFont('Helvetica', 9)
                                
                        y=y-3
                except:
                        pass

        #HSN COde
        if hsn_code != '':
                try:
                        hsn_code_word_list = material_wrapper.wrap('HSN Code :' + hsn_code)
                        for element in hsn_code_word_list:
                
                                pdf.drawString(40,y-10,element)
                                y = y - 11

                                #Page Break
                                if y < 50:
                                        y = add_new_page(pdf,po_number)
                                        y = Add_Table_Header(pdf,y)
                                        pdf.setFont('Helvetica', 9)
                                
                        y=y-3
                except:
                        pass

        y = y - 10
        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                y = Add_Table_Header(pdf,y)
                
        pdf.setFont('Helvetica-Bold', 8)

        pdf.drawString(350,y,"Total Basic Value")
        pdf.drawString(490,y,"INR " + total_discounted_price)
        y = y - 10
        
        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                y = Add_Table_Header(pdf,y)
                
        pdf.setFont('Helvetica-Bold', 8)
        pdf.drawString(350,y,"GST "+ str(gst) + " %")
        pdf.drawString(490,y,"INR " + str(gst_value))
        y = y - 10

        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                y = Add_Table_Header(pdf,y)
                
        pdf.setFont('Helvetica-Bold', 8)
        pdf.rect(350,y,228,0.2, stroke=1, fill=1)
        y = y - 10

        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                y = Add_Table_Header(pdf,y)
        
        pdf.setFont('Helvetica-Bold', 8)

        pdf.drawString(350,y,"Total")
        pdf.drawString(490,y,"INR " + str(total_value))
        y = y - 5
        pdf.rect(10,y,568,0.1, stroke=1, fill=1)
        y = y - 10
        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                y = Add_Table_Header(pdf,y)
        return(y)

#Add pricing Amount
def add_pricing_amount(pdf,po_number,state,y,total_basic_amount,total_gst,freight_charges,pf,custom_duties,insurance,grand_total):
        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 9)
        pdf.setFont('Helvetica-Bold', 8)

        pdf.drawString(330,y,"All Total Basic Value")
        pdf.drawString(490,y,"INR " + total_basic_amount)
        y = y - 10

        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 9)
        pdf.setFont('Helvetica-Bold', 8)

        if state.upper() == 'KARNATAKA':
                if y < 50:
                        y = add_new_page(pdf,po_number)
                        pdf.setFont('Helvetica', 9)
                pdf.setFont('Helvetica-Bold', 8)
                
                pdf.drawString(330,y,"Total Applicable CGST Value")
                pdf.drawString(490,y,"INR " + str(round((float(total_gst)/2),2)))
                y = y - 10

                if y < 50:
                        y = add_new_page(pdf,po_number)
                        pdf.setFont('Helvetica', 9)
                pdf.setFont('Helvetica-Bold', 8)

                pdf.drawString(330,y,"Total Applicable SGST Value")
                pdf.drawString(490,y,"INR " + str(round((float(total_gst)/2),2)))
                y = y - 10

        else:
                if y < 50:
                        y = add_new_page(pdf,po_number)
                        pdf.setFont('Helvetica', 9)
                pdf.setFont('Helvetica-Bold', 8)
                
                pdf.drawString(330,y,"Total Applicable IGST Value")
                pdf.drawString(490,y,"INR " + str(round((float(total_gst)),2)))
                y = y - 10 

        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 9)
        pdf.setFont('Helvetica-Bold', 8)

        if freight_charges != "0.00":
                pdf.drawString(330,y,"Freight Charges")
                pdf.drawString(490,y,"INR " + freight_charges)
                y = y - 10

        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 9)
        pdf.setFont('Helvetica-Bold', 8)

        if pf != "0.00":
                pdf.drawString(330,y,"Packaging and Forwarding Charges")
                pdf.drawString(490,y,"INR " + pf)
                y = y - 10

        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 9)
        pdf.setFont('Helvetica-Bold', 8)

        if insurance != "0.00":
                pdf.drawString(330,y,"Insurance")
                pdf.drawString(490,y,"INR " + insurance)
                y = y - 10

        y = y + 5
        pdf.rect(330,y,248,0.1, stroke=1, fill=1)
        y = y -10

        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 9)
        pdf.setFont('Helvetica-Bold', 8)

        pdf.drawString(330,y,"Grand Total")
        pdf.drawString(490,y,"INR " + grand_total)
        y = y - 10
        return(y)

def add_amount_in_word(pdf,y,po_number,amount):
        #Page Break
        if y < 50:
                y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 9)

        pdf.rect(10,y,570,0.1, stroke=1, fill=1)
        wrapper = textwrap.TextWrapper(width=160) 
        word_list = wrapper.wrap(text=amount)
        y = y - 11
        pdf.setFillColor(HexColor('#000000'))
        pdf.setFont('Helvetica-Bold', 8)
        for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 8
        pdf.rect(10,y,570,0.1, stroke=1, fill=1)
        y = y - 8
        return(y)

#Add Comments
def add_comments(pdf,y,po_number,comments):
        if comments != "":
                try:
                        comments = '*** Special Notes :: ' + comments
                        pdf.setFont('Helvetica-Bold', 8)
                        wrapper = textwrap.TextWrapper(width=160) 
                        word_list = wrapper.wrap(text=comments)
                        for element in word_list:
                                pdf.drawString(10,y,element)
                                y = y - 8
                except:
                        pass
        return(y)

#Terms and Conditions
def add_terms_conditions(pdf,y,po_number,mode_of_transport,installation,inco_terms,terms_of_payment):
        pdf.setFillColor(HexColor('#E4E4E4'))
        y = y -15
        pdf.rect(10,y,570,15, stroke=0, fill=1)
        #Colum headers
        pdf.setFillColor(HexColor('#000000'))
        pdf.setFont('Helvetica-Bold', 8)
        pdf.drawString(12,y + 5,'Terms and Conditions')
        y = y -10
        
        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)
        
                pdf.setFont('Helvetica', 8)
                pdf.drawString(12,y,'Inco Terms : ' + inco_terms)
                y = y - 10
        except:
                pass

        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 8)
                pdf.drawString(12,y,'Mode of Transport : ' + mode_of_transport)
                y = y - 10
        except:
                pass

        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 8)
                pdf.drawString(12,y,'Installation : ' + installation)
                y = y - 10
        except:
                pass

        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 8)
                pdf.drawString(12,y,'Terms of Payment : ' + terms_of_payment)
                y = y - 10
        except:
                pass

        return(y)

#Delivery Instruction
def add_delivery_instruction(pdf,y,po_number,di1,di2,di3,di4,di5,di6,di7,di8,di9,di10):
        pdf.setFillColor(HexColor('#E4E4E4'))
        y = y -15
        pdf.rect(10,y,570,15, stroke=0, fill=1)
        #Colum headers
        pdf.setFillColor(HexColor('#000000'))
        pdf.setFont('Helvetica-Bold', 8)
        pdf.drawString(12,y + 5,'Delivery Instruction')
        y = y -10

        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)

                if di1 != '':
                        pdf.setFont('Helvetica', 8)
                        pdf.drawString(12,y,di1)
                        y = y - 10
        except:
                pass

        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)

                if di2 != '':
                        pdf.setFont('Helvetica', 8)
                        pdf.drawString(12,y,di2)
                        y = y - 10
        except:
                pass

        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)

                if di3 != '':
                        pdf.setFont('Helvetica', 8)
                        pdf.drawString(12,y,di3)
                        y = y - 10
        except:
                pass

        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)

                if di4 != '':
                        pdf.setFont('Helvetica', 8)
                        pdf.drawString(12,y,di4)
                        y = y - 10
        except:
                pass

        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)

                if di5 != '':
                        pdf.setFont('Helvetica', 8)
                        pdf.drawString(12,y,di5)
                        y = y - 10
        except:
                pass

        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)

                if di6 != '':
                        pdf.setFont('Helvetica', 8)
                        pdf.drawString(12,y,di6)
                        y = y - 10
        except:
                pass


        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)

                if di7 != '':
                        pdf.setFont('Helvetica', 8)
                        pdf.drawString(12,y,di7)
                        y = y - 10
        except:
                pass

        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)

                if di8 != '':
                        pdf.setFont('Helvetica', 8)
                        pdf.drawString(12,y,di8)
                        y = y - 10
        except:
                pass


        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)

                if di9 != '':
                        pdf.setFont('Helvetica', 8)
                        pdf.drawString(12,y,di9)
                        y = y - 10
        except:
                pass


        try:
                #Page Break
                if y < 50:
                        y = add_new_page(pdf,po_number)

                if di10 != '':
                        pdf.setFont('Helvetica', 8)
                        pdf.drawString(12,y,di10)
                        y = y - 10
        except:
                pass
        return(y)

#add requester
def add_requester(pdf,y,po_number,requester_name,email,phone):
        #Page Break
        if y < 100:
                y = add_new_page(pdf,po_number)
                pdf.setFont('Helvetica', 9)
        pdf.setFont('Helvetica-Bold', 8)

        try:
                pdf.drawString(400,y,"Requester :")
                pdf.drawString(450,y,requester_name)
                y = y - 10
        except:
                y = y - 10
        
        try:
                pdf.drawString(400,y,"Email :")
                pdf.drawString(450,y,email)
                y = y - 10
        except:
                y = y - 10
        
        try:
                pdf.drawString(400,y,"Contact No:")
                pdf.drawString(450,y,phone)
                y = y - 10
        except:
                y = y - 20

        try:
                pdf.drawString(170,y,"[ THIS IS A SYSTEM GENERATED PURCHASE ORDER ]")
                y = y - 10
        except:
                y = y - 10
        return(y)        


#Create PDF
def PO_Generator(po_number):  
        #Extract PO Data
        vpo_tracker_object = VendorPOTracker.objects.get(po_number = po_number)
        vpo_object = vpo_tracker_object.vpo
        state = vpo_tracker_object.vpo.vendor.state
        vpo_lineitems = VendorPOLineitems.objects.filter(vpo = vpo_object)
        pdf = canvas.Canvas("media/po/" + po_number + ".pdf", pagesize=A4)
        pdf.setTitle(po_number + '.pdf')
        Add_Header(pdf)
        Add_Footer(pdf)
        po_information(
                pdf,
                vpo_tracker_object.po_number,
                vpo_tracker_object.po_date,
                vpo_object.delivery_date,
                vpo_object.offer_reference,
                vpo_object.offer_date,
                vpo_object.vendor.id
        )
        y = Add_To(
                pdf,
                vpo_object.vendor.name,
                vpo_object.vendor.address,
                vpo_object.vendor.gst_number,
                vpo_object.shipping_address,
                vpo_object.billing_address
        )
        y = Add_Receiver(
                pdf,
                y,
                vpo_object.receiver_name,
                vpo_object.receiver_phone1,
                vpo_object.receiver_phone2,
                vpo_object.receiver_dept,
        )
        y = Add_grt(
                pdf,
                y,
                vpo_object.vendor_contact_person.name
        )
        y = Add_Table_Header(pdf,y)
        i = 1
        total_basic_amount = 0
        total_gst = 0
        for lineitem in vpo_lineitems:
                product_title = lineitem.product_title
                description = lineitem.description
                model = lineitem.model
                brand = lineitem.brand
                product_code = lineitem.product_code

                hsn_code = lineitem.hsn_code
                gst = lineitem.gst

                quantity = lineitem.quantity
                uom = lineitem.uom

                unit_price = '{0:.2f}'.format(lineitem.unit_price)
                discount = '{0:.2f}'.format(lineitem.discount)
                discounted_price = '{0:.2f}'.format(float(unit_price) - (float(unit_price)*float(discount)/100))
                total_discounted_price = '{0:.2f}'.format(float(discounted_price)*float(quantity))
                gst_value = '{0:.2f}'.format(float(total_discounted_price)*float(gst)/100)
                total_value = '{0:.2f}'.format(float(total_discounted_price) + float(gst_value))

                total_basic_amount = total_basic_amount + float(total_discounted_price)
                total_gst = total_gst + float(gst_value)
                
                y = add_lineitem(
                        pdf,
                        y,
                        i,
                        po_number,
                        product_title,
                        description,
                        model,
                        brand,
                        product_code,
                        hsn_code,
                        gst,
                        quantity,
                        uom,
                        unit_price,
                        discount,
                        discounted_price,
                        total_discounted_price,
                        gst_value,
                        total_value)
                i = i + 1

        grand_total = total_basic_amount + total_gst + vpo_object.freight_charges + vpo_object.pf + vpo_object.insurance + vpo_object.custom_duties        
        y = add_pricing_amount(
                pdf,
                po_number,
                state,
                y,
                '{0:.2f}'.format(total_basic_amount),
                '{0:.2f}'.format(total_gst),
                '{0:.2f}'.format(vpo_object.freight_charges),
                '{0:.2f}'.format(vpo_object.pf),
                '{0:.2f}'.format(vpo_object.custom_duties),
                '{0:.2f}'.format(vpo_object.insurance),
                '{0:.2f}'.format(grand_total)
        )
        words = num2words('{0:.2f}'.format(grand_total))
        y = add_amount_in_word(pdf, y,po_number,'Amount In Words : ' + words.title() + ' Rupees only')
        y = add_comments(pdf,y,po_number,vpo_object.comments)
        y = add_terms_conditions(
                pdf,
                y,
                po_number,
                vpo_object.mode_of_transport,
                vpo_object.installation,
                vpo_object.inco_terms,
                vpo_object.terms_of_payment
        )
        y = add_delivery_instruction(
                pdf,
                y,
                po_number,
                vpo_object.di1,
                vpo_object.di2,
                vpo_object.di3,
                vpo_object.di4,
                vpo_object.di5,
                vpo_object.di6,
                vpo_object.di7,
                vpo_object.di8,
                vpo_object.di9,
                vpo_object.di10
        )
        y = add_requester(
                pdf,
                y,
                po_number,
                vpo_object.requester.first_name + ' ' + vpo_object.requester.last_name,
                vpo_object.requester.email,
                vpo_object.requester.profile.office_mobile)
        pdf.showPage()
        pdf.save()

#VPO Generate PO
class VPOGeneratePO(APIView):
        parser_classes = (JSONParser,)

        #Check Authentications
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated,]

        def get(self, request, format=None, po_number=None):
                PO_Generator(po_number)
                return Response({'po_url' : '/api/media/po/' + po_number + '.pdf'})



#VPO Approved Ready List
@login_required(login_url="/employee/login/")
def VPOApprovedReadyList(request):
        context={}
        context['PO'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == 'GET':
                if type == 'Sourcing':
                        vpo_list = VendorPOTracker.objects.filter(status='Approved',vpo__requester=u)
                        context['vpo_list'] = vpo_list
                        return render(request,"Sourcing/VPO/approval_list.html",context)

                if type == 'Sales':
                        vpo_list = VendorPOTracker.objects.filter(status='Approved')
                        context['vpo_list'] = vpo_list
                        return render(request,"Sales/VPO/ready_approval_list.html",context)

#VPO Approved Ready List
@login_required(login_url="/employee/login/")
def VPOApprovedReadyLineitems(request,po_number):
        context={}
        context['PO'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == 'GET':
                vpo = VendorPOTracker.objects.get(po_number=po_number)
                vpo_lineitem = VendorPOLineitems.objects.filter(vpo=vpo.vpo)
                context['vpo'] = vpo
                context['vpo_lineitem'] = vpo_lineitem
                PO_Generator(po_number)

                if type == 'Sourcing':
                        return render(request,"Sourcing/VPO/vpo_lineitem.html",context)   

                if type == 'Sales':
                        vpo_status = VPOStatus.objects.filter(vpo = vpo)
                        context['vpo_status'] = vpo_status
                        return render(request,"Sales/VPO/ready_vpo_lineitem.html",context)                


#VPO Approved change info
@login_required(login_url="/employee/login/")
def VPOApprovedChangeData(request,po_number):
        context={}
        context['PO'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == 'POST':
                vpo_tracker = VendorPOTracker.objects.get(po_number=po_number)
                vpo_tracker.status = 'Rejected' 
                vpo_tracker.vpo.po_status = 'Rejected'
                vpo_tracker.vpo.cpo.status = 'approved'
                vpo_tracker.vpo.cpo.save()
                vpo_tracker.vpo.save()
                vpo_tracker.save()

                return HttpResponseRedirect(reverse('vpo-approved-ready-list'))


#VPO Approved change info
@login_required(login_url="/employee/login/")
def VPOUpdateStatus(request,po_number):
        context={}
        context['PO'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == 'POST':
                data = request.POST
                
                vpo = VendorPOTracker.objects.get(po_number=po_number)
                vpo.order_status = data['order_status']
                vpo.remarks = data['remarks']
                vpo.save()

                VPOStatus.objects.create(
                        vpo = vpo,
                        order_status = data['order_status'],
                        remarks = data['remarks']
                )

                return HttpResponseRedirect(reverse('vpo-approved-ready-list'))

