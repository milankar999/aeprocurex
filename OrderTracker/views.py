from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from State.models import StateList
from POFromCustomer.models import *
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
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
from django.core import mail
from django.conf import settings
from babel.numbers import format_currency

#Pending Order List
@login_required(login_url="/employee/login/")
def pending_cpo_list(request):
    context={}
    context['order_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
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

        total_basic_pending = 0
        total_pending = 0
        for item in pending_cpo_list:
            #print(item['total_value'])
            total_basic_pending = total_basic_pending + float(item['total_basic_value'])
            total_pending = total_pending + float(item['total_value'])

            #print(total_basic_pending)
            #print(total_pending)

        context['total_basic_pending'] = format_currency(total_basic_pending, 'INR', locale='en_IN')
        context['total_pending'] = format_currency(total_pending, 'INR', locale='en_IN')

        if type == 'Sales':
            return render(request,"Sales/OrderTracker/pending_order_list.html",context)

        if type == 'CRM':
            return render(request,"CRM/OrderTracker/pending_order_list.html",context)

#Pending order details
@login_required(login_url="/employee/login/")
def pending_cpo_lineitems(request,cpo_id=None):
    context={}
    context['order_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        pending_cpo = CustomerPO.objects.get(id=cpo_id)
        cpo_lineitem = CPOLineitem.objects.filter(cpo = pending_cpo)
        context['cpo'] = pending_cpo
        context['pending_cpo_lineitem'] = cpo_lineitem

        if type == 'Sales':
            return render(request,"Sales/OrderTracker/pending_cpo_lineitem.html",context)
            
        if type == 'CRM':
            return render(request,"CRM/OrderTracker/pending_cpo_lineitem.html",context)

#Pending order details
@login_required(login_url="/employee/login/")
def change_quantity_view(request,cpo_id=None):
    context={}
    context['order_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        pending_cpo = CustomerPO.objects.get(id=cpo_id)
        cpo_lineitem = CPOLineitem.objects.filter(cpo = pending_cpo)
        context['cpo'] = pending_cpo
        context['pending_cpo_lineitem'] = cpo_lineitem

        if type == 'CRM':
            return render(request,"CRM/OrderTracker/pending_cpo_lineitem_change.html",context)

#Pending order details
@login_required(login_url="/employee/login/")
def cpo_delivery_qty_update(request,cpo_id=None,lineitem_id=None):
    context={}
    context['order_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        item = CPOLineitem.objects.get(id = lineitem_id)
        context['item'] = item

        if type == 'CRM':
            return render(request,"CRM/OrderTracker/quantity_edit.html",context)

    if request.method == "POST":
        data = request.POST
        item = CPOLineitem.objects.get(id = lineitem_id)
        item.pending_delivery_quantity = data['pending_quantity']

        item.save()

        return HttpResponseRedirect(reverse('order-tracker-change-quantity',args=[cpo_id]))