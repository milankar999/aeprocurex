from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from State.models import StateList
from RFP.models import *
from Sourcing.models import *
from COQ.models import  *
from Customer.models import *
from POFromCustomer.models import *
import random
from django.db.models import F
import textwrap
import datetime
import os
from django.views.static import serve
from django.http import FileResponse
from django.db.models import Q

@login_required(login_url="/employee/login/")
def purchare_order_selection(request):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                processing_count = InvoiceTracker.objects.filter(generating_status='creation_in_progress').count()

                if processing_count > 0:
                        processing_invoice_list = InvoiceTracker.objects.filter(generating_status='creation_in_progress')
                        context['processing_invoicce_list'] = processing_invoice_list
                        return render(request,"Accounts/Invoice/invoice_processing_list.html",context)

                cpo_list = CustomerPO.objects.filter(Q(status='direct_processing') | Q(status = 'po_processed') | Q(status = 'Full_Product_Received'))
                context['cpo_list'] = cpo_list

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/purchase_order_selection.html",context)

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


@login_required(login_url="/employee/login/")
def invoice_lineitem_selection(request,cpo_id=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                cpo = CustomerPO.objects.get(id=cpo_id)
                cpo_lineitem = CPOLineitem.objects.filter(cpo=cpo)
                if cpo.lineitem_copy_status == False:
                        for item in cpo_lineitem:
                                PendingDelivery.objects.create(
                                        cpo_lineitem = item,
                                        pending_quantity = item.quantity
                                )
                        cpo.lineitem_copy_status = True
                        cpo.save()
                
                pending_delivery = PendingDelivery.objects.filter(cpo_lineitem__cpo = cpo)
                context['pending_delivery'] = pending_delivery
                context['cpo_lineitem'] = cpo_lineitem
                
                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/invoice_pending_lineitem.html",context)

        if request.method == 'POST':
                data = request.POST
                items = data['item_list'] 
                item_list = items.split(",")

                cpo = CustomerPO.objects.get(id=cpo_id)
                financial_year = get_financial_year(datetime.datetime.today().strftime('%Y-%m-%d'))
                invoice_count = (InvoiceTracker.objects.filter(financial_year = financial_year).count()) + 1
                invoice_no = 'AP' + financial_year + "{:04d}".format(invoice_count)
                print(invoice_no)
                invoice_obj = InvoiceTracker.objects.create(
                        invoice_no = invoice_no,
                        cpo = cpo,
                        customer = cpo.customer,
                        customer_contact_person = cpo.customer_contact_person,
                        billing_address = cpo.billing_address,
                        shipping_address = cpo.shipping_address,
                        po_reference = cpo.customer_po_no,
                        po_date = cpo.customer_po_date,
                        financial_year = financial_year
                )

                invoice_total_basic = 0
                invoice_total = 0

                for item in item_list:
                        if item != '':
                                pending_item_obj = PendingDelivery.objects.get(id = item)

                                total_basic_value = round((pending_item_obj.cpo_lineitem.unit_price * pending_item_obj.pending_quantity),2)
                                total_value = round((total_basic_value + (total_basic_value * pending_item_obj.cpo_lineitem.gst /100 )),2)
                                InvoiceLineitem.objects.create(
                                        invoice = invoice_obj,
                                        product_title = pending_item_obj.cpo_lineitem.product_title,
                                        description = pending_item_obj.cpo_lineitem.description,
                                        model = pending_item_obj.cpo_lineitem.model,
                                        brand = pending_item_obj.cpo_lineitem.brand,
                                        product_code = pending_item_obj.cpo_lineitem.product_code,
                                        part_number = pending_item_obj.cpo_lineitem.part_no,
                                        hsn_code = pending_item_obj.cpo_lineitem.hsn_code,
                                        quantity = pending_item_obj.pending_quantity,
                                        uom = pending_item_obj.cpo_lineitem.uom,
                                        unit_price = pending_item_obj.cpo_lineitem.unit_price,
                                        total_basic_price = total_basic_value,
                                        total_price = total_value,
                                        gst = pending_item_obj.cpo_lineitem.gst
                                )
                                invoice_total_basic = invoice_total_basic + total_basic_value 
                                invoice_total = invoice_total + total_value
                
                invoice_obj.basic_value = round(invoice_total_basic,2)
                invoice_obj.total_value = round(invoice_total,2)
                invoice_obj.save()

                return JsonResponse({"invoice_no" : invoice_no})

@login_required(login_url="/employee/login/")
def invoice_selected_lineitem(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                invoice = InvoiceTracker.objects.get(invoice_no=invoice_no)
                invoice_lineitem = InvoiceLineitem.objects.filter(invoice = invoice)
                context['invoice_lineitem'] = invoice_lineitem
                context['invoice_no'] = invoice_no

                context['invoice_total_basic'] = invoice.basic_value
                context['invoice_total_gst'] = round((invoice.total_value - invoice.basic_value),2)
                context['invoice_total'] = invoice.total_value

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/invoice_selected_lineitem.html",context)

@login_required(login_url="/employee/login/")
def invoice_delete(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                if invoice.generating_status != 'creation_in_progress':
                        return HttpResponseRedirect(reverse('invoice-selected-lineitem',args=[invoice_no]))

                else:
                        invoice.delete()
                        return HttpResponseRedirect(reverse('invoice-creation-purchase-order-selection'))

@login_required(login_url="/employee/login/")
def customer_selection(request):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                customer = CustomerProfile.objects.all()
                context['CustomerList'] = customer
                
                if type == 'Sales':
                        return render(request,"Sales/Invoice/customer_selection.html",context)

@login_required(login_url="/employee/login/")
def invoice_selected_lineitem_edit(request,invoice_no=None,lineitem_id=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                item = InvoiceLineitem.objects.get(id = lineitem_id)
                context['item'] = item

                print(item)

                if type == 'Sales':
                        return render(request,"Sales/Invoice/invoice_lineitem_edit.html",context)

        if request.method == 'POST':
                data = request.POST
                item = InvoiceLineitem.objects.get(id = lineitem_id)

                item.product_title = data['product_title']
                item.description = data['description']
                item.model = data['model']
                item.brand = data['brand']
                item.product_code = data['product_code']
                item.part_number = data['part_number']
                item.hsn_code = data['hsn_code']
                item.quantity = data['quantity']
                item.uom = data['uom']
                item.unit_price = data['unit_price']
                item.gst = data['gst']

                total_basic_price = round((float(data['unit_price']) * float(data['quantity'])),2)
                total_price = round((total_basic_price + (total_basic_price * float(data['gst'])/100)),2)

                item.total_basic_price = total_basic_price
                item.total_price = total_price

                item.save()

                invoice_obj = InvoiceTracker.objects.get(invoice_no=invoice_no)
                invoice_lineitems = InvoiceLineitem.objects.filter(invoice = invoice_obj)

                invoice_total_basic = 0
                invoice_total = 0

                for item in invoice_lineitems:
                        invoice_total_basic = invoice_total_basic + item.total_basic_price
                        invoice_total = invoice_total + item.total_price

                invoice_obj.basic_value = round(invoice_total_basic,2)
                invoice_obj.total_value = round(invoice_total,2)

                invoice_obj.save()

                return HttpResponseRedirect(reverse('invoice-selected-lineitem',args=[invoice_no]))

@login_required(login_url="/employee/login/")
def invoice_selected_lineitem_delete(request,invoice_no=None,lineitem_id=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                item = InvoiceLineitem.objects.get(id = lineitem_id)
                context['item'] = item

                print(item)

                if type == 'Sales':
                        return render(request,"Sales/Invoice/invoice_lineitem_delete.html",context)

        if request.method == 'POST':
                data = request.POST
                item = InvoiceLineitem.objects.get(id = lineitem_id)
                item.delete()

                invoice_obj = InvoiceTracker.objects.get(invoice_no=invoice_no)
                invoice_lineitems = InvoiceLineitem.objects.filter(invoice = invoice_obj)

                invoice_total_basic = 0
                invoice_total = 0

                for item in invoice_lineitems:
                        invoice_total_basic = invoice_total_basic + item.total_basic_price
                        invoice_total = invoice_total + item.total_price

                invoice_obj.basic_value = round(invoice_total_basic,2)
                invoice_obj.total_value = round(invoice_total,2)

                invoice_obj.save()

                return HttpResponseRedirect(reverse('invoice-selected-lineitem',args=[invoice_no]))





