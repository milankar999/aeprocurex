from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from State.models import StateList
from POFromCustomer.models import *
from POForVendor.models import *
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

#Pending order details
@login_required(login_url="/employee/login/")
def cpo_to_vew_supplier_order(request,cpo_id=None):
    context={}
    context['order_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        customer_po = CustomerPO.objects.get(id = cpo_id)
        
        vendor_po_list = VendorPOTracker.objects.filter(vpo__cpo = customer_po).values(
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

        vendor_po_lineitem = VendorPOLineitems.objects.filter(vpo__cpo = customer_po).values(
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

        
        return render(request,"Sales/OrderTracker/cpo_to_vendor_po_list.html",context)


def refrech_cpo_calculation(cpo_id):
    cpo = CustomerPO.objects.get(id = cpo_id)
    cpo_lineitem = CPOLineitem.objects.filter(cpo = cpo)
    
    total_basic_value = 0
    total_value = 0

    for item in cpo_lineitem:
        basic_price = round((item.quantity * item.unit_price),2)
        
        if cpo.customer.tax_type == 'SEZ':
            total_price = basic_price
        else:
            total_price = round((basic_price + round((basic_price * item.gst / 100),2)),2)

        item.total_basic_price = basic_price
        item.total_price = total_price

        item.save()

        total_basic_value = total_basic_value + basic_price
        total_value = total_value + total_price

    cpo.total_basic_value = round(total_basic_value,2)
    cpo.total_value = round(total_value,2)
    cpo.save()


#Edit order details
@login_required(login_url="/employee/login/")
def change_order_details(request,cpo_id=None):
    context={}
    context['order_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if request.method == 'GET':
        pending_cpo = CustomerPO.objects.get(id=cpo_id)
        cpo_lineitem = CPOLineitem.objects.filter(cpo = pending_cpo)
        context['cpo'] = pending_cpo
        context['cpo_lineitem'] = cpo_lineitem

        if u.profile.cpo_editing == 'yes':
            return render(request,"CRM/OrderTracker/EditPO/selected_lineitem.html",context)
            
        else:
            return JsonResponse({'Message': 'You are not allow to view this page'})

    if request.method == 'POST':
        cpo = CustomerPO.objects.get(id=cpo_id)
        data = request.POST

        cpo.customer_po_no = data['customer_po_no']
        
        try:
            if str(data['customer_po_date']) != '':
                cpo.customer_po_date = data['customer_po_date']
        except:
            pass

        try:
            if str(data['delivery_date']) != '':
                cpo.delivery_date = data['delivery_date']
        except:
            pass
        
        cpo.billing_address = data['billing_address']
        cpo.shipping_address = data['shipping_address']
        cpo.inco_terms = data['inco_terms']
        cpo.payment_terms = data['payment_terms']
        cpo.po_type = data['po_type']

        try:
            cpo.document1 = request.FILES['supporting_document1']
        except:
            pass

        try:
            cpo.document2 = request.FILES['supporting_document2']
        except:
            pass

        cpo.save()
        return render(request,"CRM/OrderTracker/EditPO/success.html",context)


#Add new Item
@login_required(login_url="/employee/login/")
def change_order_add_new_item(request, cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                data = request.POST
                cpo = CustomerPO.objects.get(id=cpo_id)
                total_basic_price = round((float(data['quantity']) * float(data['unit_price'])),2)
                total_price = round((total_basic_price + (total_basic_price * float(data['gst']) / 100)),2) 
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
                        total_basic_price = total_basic_price,
                        total_price = total_price,
                        pending_po_releasing_quantity = data['quantity'],
                        pending_delivery_quantity = data['quantity'],
                )
                refrech_cpo_calculation(cpo_id)
                return HttpResponseRedirect(reverse('order-tracker-change-order-details',args=[cpo_id]))


#Lineitem Edit
@login_required(login_url="/employee/login/")
def change_order_lineitem_edit(request, cpo_id=None, lineitem_id = None):
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
                        return render(request,"CRM/OrderTracker/EditPO/lineitem_edit.html",context)

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

                refrech_cpo_calculation(cpo_id)
                return HttpResponseRedirect(reverse('order-tracker-change-order-details',args=[cpo_id]))


#Change Customer
@login_required(login_url="/employee/login/")
def change_order_customer_selection(request, cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
            customer_list = CustomerProfile.objects.all().values(
                'id',
                'name',
                'location',
                'code',
                'address'
            )
            context['customer_list'] = customer_list
            context['cpo_id'] = cpo_id

            return render(request,"CRM/OrderTracker/EditPO/change_customer.html",context)

#Change Customer
@login_required(login_url="/employee/login/")
def change_order_change_customer(request, cpo_id=None, customer_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
            customer = CustomerProfile.objects.get(id = customer_id)
            context['customer'] = customer

            return render(request,"CRM/OrderTracker/EditPO/customer_confirmation.html",context)

        if request.method == 'POST':
            cpo = CustomerPO.objects.get(id = cpo_id)
            customer = CustomerProfile.objects.get(id = customer_id)

            cpo.customer = customer
            cpo.save()

            return HttpResponseRedirect(reverse('order-tracker-change-order-details',args=[cpo_id]))

#Change Contact person
@login_required(login_url="/employee/login/")
def change_order_contact_person_selection(request, cpo_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
            cpo = CustomerPO.objects.get(id = cpo_id)
            contact_person_list = CustomerContactPerson.objects.filter(customer_name = cpo.customer).values(
                'id',
                'name',
                'email1',
                'mobileNo1'
            )
            context['contact_person_list'] = contact_person_list
            context['cpo_id'] = cpo_id

            return render(request,"CRM/OrderTracker/EditPO/change_contact_person.html",context)

#Change Contact Person
@login_required(login_url="/employee/login/")
def change_order_change_contact_person(request, cpo_id=None, contact_person_id=None):
        context={}
        context['po'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
            contact_person = CustomerContactPerson.objects.get(id = contact_person_id)
            context['contact_person'] = contact_person

            return render(request,"CRM/OrderTracker/EditPO/contact_person_confirmation.html",context)

        if request.method == 'POST':
            cpo = CustomerPO.objects.get(id = cpo_id)
            contact_person = CustomerContactPerson.objects.get(id = contact_person_id)

            cpo.customer_contact_person = contact_person
            cpo.save()

            return HttpResponseRedirect(reverse('order-tracker-change-order-details',args=[cpo_id]))

            