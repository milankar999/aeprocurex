from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from State.models import StateList
from RFP.models import *
from Sourcing.models import *
from COQ.models import  *
from Customer.models import *
import random
from django.db.models import F
import textwrap
import datetime
import os
from django.views.static import serve
from django.http import FileResponse

@login_required(login_url="/employee/login/")
def enquiry_list(request):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        enquiry = RFP.objects.all().values(
            'rfp_no',
            'rfp_creation_details__creation_date',
            'customer__name',
            'customer__location',
            'customer_contact_person__name',
            'rfp_type',
            'rfp_creation_details__created_by__username',
            'rfp_assign1__assign_to1__username',
            'opportunity_status',
            'enquiry_status').order_by('-rfp_creation_details__creation_date')
        
        context['enquiry_list'] = enquiry

        if type == 'Sales':
            return render(request,"Sales/EnquiryTracker/enquiry_list.html",context)

@login_required(login_url="/employee/login/")
def lineitem_list(request):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        lineitem_list = RFPLineitem.objects.all().values(
            'rfp_no__rfp_no',
            'rfp_no__rfp_creation_details__creation_date',
            'rfp_no__rfp_type',
            'rfp_no__enquiry_status',
            'lineitem_id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'part_no',
            'quantity',
            'uom',
            'rfp_no__customer__name',
            'rfp_no__customer__location',
            'rfp_no__rfp_keyaccounts_details__key_accounts_manager__username').order_by('-rfp_no__rfp_creation_details__creation_date')
        

        context['lineitem_list'] = lineitem_list

        if type == 'Sales':
            return render(request,"Sales/EnquiryTracker/lineitem_list.html",context)

#RFP Details
@login_required(login_url="/employee/login/")
def rfp_lineitem(request,rfp_no=None):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        rfp_lineitems = RFPLineitem.objects.filter(rfp_no=RFP.objects.get(rfp_no=rfp_no)).values(
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
            'quantity')
        context['rfp_lineitems'] = rfp_lineitems

        if type == 'Sales':
            return render(request,"Sales/EnquiryTracker/rfp_lineitems.html",context)

