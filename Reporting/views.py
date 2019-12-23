from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from State.models import StateList
from RFP.models import *
from Sourcing.models import *
from COQ.models import  *
from Quotation.models import *
from Customer.models import *
from POFromCustomer.models import *
from POForVendor.models import *
from Invoice.models import *
import random
from django.db.models import F, DurationField, ExpressionWrapper
import textwrap
import datetime
import os
from django.views.static import serve
from django.http import FileResponse
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
from django.core import mail
from django.conf import settings
from django.db.models import Count
from datetime import timedelta, datetime
import pytz


# Pending Enquiry List
@login_required(login_url="/employee/login/")
def pending_enquiry_list(request):
        context={}
        context['enquiry_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == "GET":
                enquiry = RFP.objects.filter(Q(enquiry_status='Created', opportunity_status = 'Open') | Q(enquiry_status='Approved', opportunity_status = 'Open') | Q(enquiry_status='Sourcing_Completed', opportunity_status = 'Open') | Q(enquiry_status='COQ Done', opportunity_status = 'Open')).values(
                        'rfp_no',
                        'product_heading',
                        'rfp_creation_details__creation_date',
                        'customer__name',
                        'customer__location',
                        'customer_contact_person__name',
                        'rfp_type',
                        'rfp_creation_details__created_by__username',
                        'rfp_assign1__assign_to1__username',
                        'opportunity_status',
                        'enquiry_status',
                        'current_sourcing_status',
                        'up_time').order_by('-rfp_creation_details__creation_date')
        
                utc=pytz.UTC
                for item in enquiry:
                        diff = utc.localize(datetime.now()) - item['rfp_creation_details__creation_date']
                        hrs = round((((diff.days) * 24) + (diff.seconds/3600)),2)
                        item['up_time'] = hrs


                context['enquiry_list'] = enquiry

                if type == 'Management':
                        return render(request,"Management/EnquiryTracker/pending_enquiry_list.html",context)

#All received Enquiry List
@login_required(login_url="/employee/login/")
def all_received_enquiry_list(request):
        context={}
        context['enquiry_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                enquiry = RFP.objects.all().values(
                        'rfp_no',
                        'rfp_creation_details__creation_date',
                        'product_heading',
                        'customer__name',
                        'customer__location',
                        'customer_contact_person__name',
                        'rfp_type',
                        'rfp_creation_details__created_by__username',
                        'rfp_assign1__assign_to1__username',
                        'opportunity_status',
                        'enquiry_status').order_by('-rfp_creation_details__creation_date')
                
                context['enquiry_list'] = enquiry

                if type == 'Management':
                        return render(request,"Management/EnquiryTracker/received_enquiry_list.html",context)


#Enquiry Details
@login_required(login_url="/employee/login/")
def enquiry_details(request,rfp_no=None):
        context={}
        context['enquiry_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == "GET":
                
                rfp = RFP.objects.get(rfp_no=rfp_no)
                rfp_lineitems = RFPLineitem.objects.filter(rfp_no=rfp).values(
                        'product_title',
                        'description',
                        'model',
                        'brand',
                        'product_code',
                        'part_no',
                        'category',
                        'hsn_code',
                        'gst',
                        'uom',
                        'target_price',
                        'quantity')
                
                if rfp.rfp_type == 'PSP':
                        psp_enquiry_value = 0
                        for item in rfp_lineitems:
                                psp_enquiry_value = psp_enquiry_value + item['target_price']
                        context['psp_enquiry_value'] = psp_enquiry_value

                context['rfp'] = rfp
                context['rfp_lineitems'] = rfp_lineitems

                if type == 'Management':
                        return render(request,"Management/EnquiryTracker/enquiry_details.html",context)

#Enquiry Sourcing tDetails
@login_required(login_url="/employee/login/")
def enquiry_sourcing_details(request,rfp_no=None):
        context={}
        context['enquiry_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        
        if request.method == "GET":
                
                rfp = RFP.objects.get(rfp_no=rfp_no)
                sourcing = Sourcing.objects.filter(rfp = rfp)
                sourcing_lineitem = SourcingLineitem.objects.filter(sourcing__rfp = rfp)
                supplier_quotation = SourcingAttachment.objects.filter(sourcing__rfp = rfp)
                other_charges = SourcingCharges.objects.filter(sourcing__rfp = rfp)

                context['sourcing'] = sourcing
                context['sourcing_lineitem'] = sourcing_lineitem
                context['rfp_no'] = rfp_no
                context['supplier_quotation'] = supplier_quotation
                context['other_charges'] = other_charges


                if type == 'Management':
                        return render(request,"Management/EnquiryTracker/sourcing_details.html",context)

#Enquiry Quotation Details
@login_required(login_url="/employee/login/")
def enquiry_quotation_details(request,rfp_no=None):
        context={}
        context['enquiry_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                rfp = RFP.objects.get(rfp_no=rfp_no)
                quotation_list = QuotationTracker.objects.filter(rfp = rfp)
                quotation_lineitem = QuotationLineitem.objects.filter(quotation__rfp = rfp)

                context['quotation_list'] = quotation_list
                context['quotation_lineitem'] = quotation_lineitem
                context['rfp_no'] = rfp_no

                if type == 'Management':
                        return render(request,"Management/EnquiryTracker/quotation_details.html",context)


##Generated Quotation Tracker
@login_required(login_url="/employee/login/")
def generated_quotation_list(request):
        context={}
        context['quotation_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                quotation = QuotationTracker.objects.all().values(
                        'quotation_no',
                        'quotation_date',
                        'rfp__rfp_no',
                        'customer__name',
                        'customer_contact_person__name',
                        'status',
                        'enquiry_reference',
                        'rfp__rfp_type',
                        'total_basic_price',
                        'total_price',
                        'rfp__product_heading'
                )
                context['quotation'] = quotation

                if type == 'Management':
                        return render(request,"Management/QuotationTracker/quotation_list.html",context)

#Quotation Lineitem
@login_required(login_url="/employee/login/")
def generated_quotation_details(request,quotation_no=None):
        context={}
        context['quotation_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                quotation = QuotationTracker.objects.get(quotation_no = quotation_no)
                quotation_lineitem = QuotationLineitem.objects.filter(quotation = quotation)

                context['quotation'] = quotation
                context['quotation_lineitem'] = quotation_lineitem

                if type == 'Management':
                        return render(request,"Management/QuotationTracker/quotation_details.html",context)

#Received Quotation Tracker
@login_required(login_url="/employee/login/")
def received_quotation_list(request):
        context={}
        context['quotation_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                sourcing = Sourcing.objects.all().values(
                        'id',
                        'rfp__rfp_no',
                        'supplier__name',
                        'supplier__location',
                        'supplier_contact_person__name',
                        'offer_reference',
                        'offer_date',
                        'rfp__product_heading'
                )
                context['sourcing'] = sourcing

                if type == 'Management':
                        return render(request,"Management/QuotationTracker/supplier_quotation_list.html",context)

#Received Quotation Details
@login_required(login_url="/employee/login/")
def received_quotation_details(request,sourcing_id=None):
        context={}
        context['quotation_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                sourcing = Sourcing.objects.get(id = sourcing_id)
                sourcing_lineitem = SourcingLineitem.objects.filter(sourcing=sourcing)

                supplier_quotation = SourcingAttachment.objects.filter(sourcing = sourcing)
                other_charges = SourcingCharges.objects.filter(sourcing = sourcing)

                context['sourcing'] = sourcing
                context['sourcing_lineitem'] = sourcing_lineitem
                context['supplier_quotation'] = supplier_quotation
                context['other_charges'] = other_charges


                if type == 'Management':
                        return render(request,"Management/QuotationTracker/supplier_quotation_details.html",context)


#Pending CPO List  
@login_required(login_url="/employee/login/")
def pending_cpo_list(request):
        context={}
        context['cpo_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
                             
        if request.method == 'GET':
                pending_cpo_list = CustomerPO.objects.filter(Q(status='Created') | Q(status='approved') | Q(status='direct_processing') | Q(status = 'po_processed')).values(
                        'id',
                        'status',
                        'customer__name',
                        'customer__location',
                        'customer_contact_person__name',
                        'po_type',
                        'customer_po_no',
                        'customer_po_date',
                        'delivery_date',
                        'cpo_assign_detail__assign_to__first_name',
                        'cpo_assign_detail__assign_to__last_name',
                        'total_basic_value',
                        'total_value'
                )
                context['pending_cpo_list'] = pending_cpo_list

                if type == 'Management':
                        return render(request,"Management/CPOTracker/pending_order_list.html",context)

#All CPO List
@login_required(login_url="/employee/login/")
def all_cpo_list(request):
        context={}
        context['cpo_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                pending_cpo_list = CustomerPO.objects.all().values(
                        'id',
                        'status',
                        'customer__name',
                        'customer__location',
                        'customer_contact_person__name',
                        'po_type',
                        'customer_po_no',
                        'customer_po_date',
                        'delivery_date',
                        'cpo_assign_detail__assign_to__first_name',
                        'cpo_assign_detail__assign_to__last_name',
                        'total_basic_value',
                        'total_value'
                )
                context['pending_cpo_list'] = pending_cpo_list

                if type == 'Management':
                        return render(request,"Management/CPOTracker/all_order_list.html",context)

#CPO details
@login_required(login_url="/employee/login/")
def cpo_details(request, cpo_id = None):
        context={}
        context['cpo_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo = CustomerPO.objects.get(id = cpo_id)
                cpo_lineitem = CPOLineitem.objects.filter(cpo = cpo)

                context['cpo'] = cpo
                context['cpo_lineitem'] = cpo_lineitem

                if type == 'Management':
                        return render(request,"Management/CPOTracker/cpo_details.html",context)

#CPO Check Our Quotation Reference
@login_required(login_url="/employee/login/")
def cpo_quotation_reference(request, cpo_id = None):
        context={}
        context['cpo_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo = CustomerPO.objects.get(id = cpo_id)
                selected_quotation_list = CPOSelectedQuotation.objects.filter(customer_po = cpo)

                context['cpo'] = cpo
                context['selected_quotation_list'] = selected_quotation_list

                if type == 'Management':
                        return render(request,"Management/CPOTracker/cpo_quotation_details.html",context)

#CPO Check Our Quotation Reference
@login_required(login_url="/employee/login/")
def cpo_vendorPO_details(request, cpo_id = None):
        context={}
        context['cpo_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo = CustomerPO.objects.get(id = cpo_id)
                vendor_po_list = VendorPOTracker.objects.filter(vpo__cpo = cpo).values(
                        'vpo__id',
                        'po_number',
                        'po_date',
                        'requester',
                        'basic_value',
                        'total_value',
                        'vpo__vendor__name',
                        'vpo__vendor__location',
                        'vpo__shipping_address',
                        'vpo__delivery_date',
                        'vpo__requester__first_name',
                        'vpo__requester__last_name',
                        'vpo__terms_of_payment',
                        'vpo__currency',
                        'vpo__inr_value',
                        'non_inr_value'
                )

                vendor_po_lineitem = VendorPOLineitems.objects.filter(vpo__cpo = cpo).values(
                        'vpo__id',
                        'product_title',
                        'description',
                        'model',
                        'brand',
                        'product_code',
                        'hsn_code',
                        'gst',
                        'uom',
                        'quantity',
                        'unit_price',
                        'discount',
                        'actual_price',
                        'total_basic_price',
                        'total_price'
                )

                context['vendor_po_list'] = vendor_po_list
                context['vendor_po_lineitem'] = vendor_po_lineitem
        
                return render(request,"Management/CPOTracker/cpo_to_vendor_po_list.html",context)

#CPO Check Our Invoicing details
@login_required(login_url="/employee/login/")
def cpo_invoicing_details(request, cpo_id = None):
        context={}
        context['cpo_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo = CustomerPO.objects.get(id = cpo_id)
                cpo_lineitem = CPOLineitem.objects.filter(cpo = cpo)
                
                #Copy Pending Quantity
                if cpo.lineitem_copy_status == False:
                        for item in cpo_lineitem:
                                PendingDelivery.objects.create(
                                        cpo_lineitem = CPOLineitem.objects.get(id = item.id),
                                        pending_quantity = item.quantity,
                                        pending_indirect_quantity = item.indirect_processing_quantity
                                )
                        cpo.lineitem_copy_status = True
                        cpo.save()

                pending_delivery = PendingDelivery.objects.filter(cpo_lineitem__cpo = cpo, pending_quantity__gt = 0)
                context['pending_delivery'] = pending_delivery
                context['cpo'] = cpo

                invoice_list = InvoiceTracker.objects.filter(cpo = cpo)
                invoice_lineitems = InvoiceLineitem.objects.filter(invoice__cpo = cpo)
                context['invoice_list'] = invoice_list
                context['invoice_lineitems'] = invoice_lineitems

                if type == 'Management':
                        return render(request,"Management/CPOTracker/cpo_invoicing_details.html",context)

##OPen VPO List
@login_required(login_url="/employee/login/")
def open_vpo_list(request):
        context={}
        context['vpo_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                vpo_list = VendorPOTracker.objects.filter(status='Approved').values(
                        'po_number',
                        'vpo__vendor__name',
                        'vpo__vendor__location',
                        'po_number',
                        'po_date',
                        'vpo__cpo__customer__name',
                        'basic_value',
                        'total_value',
                        'all_total_value',
                        'vpo__currency__currency_code',
                        'vpo_type',
                        'order_status',
                        'remarks',
                        'vpo__delivery_date',
                )
                context['vpo_list'] = vpo_list
                
                if type == 'Management':
                        return render(request,"Management/VPOTracker/open_vpo_list.html",context)

#All VPO List
@login_required(login_url="/employee/login/")
def all_vpo_list(request):
        context={}
        context['vpo_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                vpo_list = VendorPOTracker.objects.all().values(
                        'po_number',
                        'vpo__vendor__name',
                        'vpo__vendor__location',
                        'po_number',
                        'po_date',
                        'vpo__cpo__customer__name',
                        'basic_value',
                        'total_value',
                        'all_total_value',
                        'vpo__currency__currency_code',
                        'vpo_type',
                        'order_status',
                        'remarks',
                        'vpo__delivery_date',
                )
                context['vpo_list'] = vpo_list
                
                if type == 'Management':
                        return render(request,"Management/VPOTracker/all_vpo_list.html",context)

#VPO Details
@login_required(login_url="/employee/login/")
def vpo_details(request, vpo_no):
        context={}
        context['vpo_tracker'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                vpo = VendorPOTracker.objects.get(po_number = vpo_no)
                vpo_lineitems = VendorPOLineitems.objects.filter(vpo = vpo.vpo)
                vpo_status = VPOStatus.objects.filter(vpo = vpo)

                context['vpo'] = vpo
                context['vpo_lineitems'] = vpo_lineitems
                context['vpo_status'] = vpo_status

                if type == 'Management':
                        return render(request,"Management/VPOTracker/vpo_details.html",context)