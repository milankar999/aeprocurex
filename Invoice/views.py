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
from GRNIR.models import *
import random
from django.db.models import F
import textwrap
import datetime
import os
from django.views.static import serve
from django.http import FileResponse
from django.db.models import Q

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import Image, Paragraph, Table, TableStyle
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap



#------------------------Invoice Based on Supplier Items Received--------------------


@login_required(login_url="/employee/login/")
def purchare_order_selection(request):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                processing_count = InvoiceTracker.objects.filter(Q(generating_status='creation_in_progress') | Q(generating_status='creation_in_progress_1')).count()

                if processing_count > 0:
                        processing_invoice_list = InvoiceTracker.objects.filter(Q(generating_status='creation_in_progress') | Q(generating_status='creation_in_progress_1'))
                        context['processing_invoicce_list'] = processing_invoice_list
                        return render(request,"Accounts/Invoice/invoice_processing_list.html",context)

                cpo_list = CustomerPO.objects.filter(Q(status = 'po_processed') | Q(status = 'Full_Product_Received') | Q(status = 'direct_processing')).values(
                        'id',
                        'customer__name',
                        'customer__location',
                        'customer__code',
                        'customer_po_no',
                        'customer_po_date',
                        'customer_contact_person__name',
                        'processing_type',
                        'total_basic_value',
                        'total_value'
                )
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
                cpo_lineitem = CPOLineitem.objects.filter(cpo=cpo).values(
                        'id',
                        'product_title',
                        'description',
                        'model',
                        'brand',
                        'product_code',
                        'part_no',
                        'uom',
                        'quantity',
                        'unit_price',
                        'total_basic_price',
                        'gst',
                        'total_price'
                )
                if cpo.lineitem_copy_status == False:
                        for item in cpo_lineitem:
                                PendingDelivery.objects.create(
                                        cpo_lineitem = CPOLineitem.objects.get(id = item['id']),
                                        pending_quantity = item['quantity']
                                )
                        cpo.lineitem_copy_status = True
                        cpo.save()
                
                pending_delivery = PendingDelivery.objects.filter(cpo_lineitem__cpo = cpo).values(
                        'cpo_lineitem__id',
                        'cpo_lineitem__product_title',
                        'cpo_lineitem__description',
                        'cpo_lineitem__model',
                        'cpo_lineitem__brand',
                        'cpo_lineitem__product_code',
                        'cpo_lineitem__part_no',
                        'pending_quantity',
                        'cpo_lineitem__uom'
                )
                context['pending_delivery'] = pending_delivery
                context['cpo_lineitem'] = cpo_lineitem
                context['total_basic_value'] = cpo.total_basic_value
                context['total_value'] = cpo.total_value
                context['po_document'] = cpo.document1

                if cpo.processing_type == 'direct':
                        grn_item = GRNLineitem.objects.filter(grn__status='completed', cpo_lineitem__cpo = cpo).values(
                                'cpo_lineitem__id',
                                'grn__grn_no',
                                'grn__vpo__vpo__vendor__name',
                                'product_title',
                                'description',
                                'model',
                                'brand',
                                'product_code',
                                'quantity',
                                'invoiced_quantity',
                                'uom'
                        )
                        context['grn_item'] = grn_item
                
                        suggested_invoicing_item = {'suggested_items':[]}
                        for item in pending_delivery:
                                if float(item['pending_quantity']) > 0:
                                        quantity = 0
                                        for g_item in grn_item:
                                                if item['cpo_lineitem__id'] == g_item['cpo_lineitem__id']:
                                                        quantity = quantity + float(g_item['quantity']) - float(g_item['invoiced_quantity'])
                                        if quantity > 0:
                                                if quantity > item['pending_quantity']:
                                                        quantity = item['pending_quantity']

                                                suggested_invoicing_item['suggested_items'].append({
                                                        'id': item['cpo_lineitem__id'],
                                                        'product_title' : item['cpo_lineitem__product_title'],
                                                        'description' : item['cpo_lineitem__description'],
                                                        'model' : item['cpo_lineitem__model'],
                                                        'brand' : item['cpo_lineitem__brand'],
                                                        'product_code' : item['cpo_lineitem__product_code'],
                                                        'part_no' : item['cpo_lineitem__part_no'],
                                                        'quantity' : quantity,
                                                        'uom' : item['cpo_lineitem__uom']
                                                })

                        print(suggested_invoicing_item)
                        context['suggested_invoicing_item'] = suggested_invoicing_item['suggested_items']

                        if type == 'Accounts':
                                return render(request,"Accounts/Invoice/invoice_pending_lineitem.html",context)

                if cpo.processing_type == 'indirect':
                        if type == 'Accounts':
                                return render(request,"Accounts/Invoice/Indirect/invoice_pending_lineitem.html",context)
        
        if request.method == 'POST':
                cpo = CustomerPO.objects.get(id=cpo_id)


                data = request.POST
                try:
                        items = data['item_list'] 
                        item_list = items.split(",")
                except:
                        pass

                processing_count = InvoiceTracker.objects.filter(Q(generating_status='creation_in_progress') | Q(generating_status='creation_in_progress_1')).count()

                if processing_count > 0:
                        return(JsonResponse({'message' : 'please complete previous invoice'}))


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


                if cpo.processing_type == 'indirect':
                        return JsonResponse({"invoice_no" : invoice_no})

                grn_item = GRNLineitem.objects.filter(grn__status='completed', cpo_lineitem__cpo = cpo).values(
                                'id',
                                'cpo_lineitem__id',
                                'grn__grn_no',
                                'quantity',
                                'invoiced_quantity',
                        )


                invoice_total_basic = 0
                invoice_total = 0

                for item in item_list:
                        if item != '':
                                id_quantity = item.split("/")
                                item_id = id_quantity[0]
                                item_quantity = float(id_quantity[1])

                                cpo_lineitem = CPOLineitem.objects.get(id = item_id)
                                pending_item_obj = PendingDelivery.objects.get(cpo_lineitem = cpo_lineitem)

                                total_basic_value = round((pending_item_obj.cpo_lineitem.unit_price * item_quantity),2)
                                total_value = round((total_basic_value + (total_basic_value * pending_item_obj.cpo_lineitem.gst /100 )),2)
                                invoice_lineitem = InvoiceLineitem.objects.create(
                                        invoice = invoice_obj,
                                        customer_po_lineitem = cpo_lineitem,
                                        product_title = pending_item_obj.cpo_lineitem.product_title,
                                        description = pending_item_obj.cpo_lineitem.description,
                                        model = pending_item_obj.cpo_lineitem.model,
                                        brand = pending_item_obj.cpo_lineitem.brand,
                                        product_code = pending_item_obj.cpo_lineitem.product_code,
                                        part_number = pending_item_obj.cpo_lineitem.part_no,
                                        hsn_code = pending_item_obj.cpo_lineitem.hsn_code,
                                        quantity = item_quantity,
                                        uom = pending_item_obj.cpo_lineitem.uom,
                                        unit_price = pending_item_obj.cpo_lineitem.unit_price,
                                        total_basic_price = total_basic_value,
                                        total_price = total_value,
                                        gst = pending_item_obj.cpo_lineitem.gst
                                )

                                invoice_total_basic = invoice_total_basic + total_basic_value 
                                invoice_total = invoice_total + total_value

                                #Cpature Inventory Diduction
                                for g_item in grn_item:
                                        print(g_item['cpo_lineitem__id'])
                                        print(item_id)
                                        
                                        gline_obj = GRNLineitem.objects.get(id = g_item['id'])
                                        if str(g_item['cpo_lineitem__id']) == item_id:
                                                InvoiceGRNLink.objects.create(
                                                        invoice_lineitem = invoice_lineitem,
                                                        grn_lineitem = gline_obj,
                                                        quantity = float(g_item['quantity']) - float(g_item['invoiced_quantity'])
                                                )
                                                
                                        print('after_if')

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

        if request.method == 'POST':
                data = request.POST
                invoice = InvoiceTracker.objects.get(invoice_no=invoice_no)

                total_basic_value = float(data['quantity']) * float(data['unit_price'])
                total_value = total_basic_value + (total_basic_value * float(data['gst']) / 100)

                InvoiceLineitem.objects.create(
                        invoice = invoice,
                        product_title = 'added_by_accounts',
                        description = data['description'],
                        hsn_code = data['hsn_code'],
                        quantity = float(data['quantity']),
                        uom = data['uom'],
                        unit_price = float(data['unit_price']),
                        total_basic_price = round(total_basic_value,2),
                        total_price = round(total_value,2),
                        gst = float(data['gst'])
                )

                invoice_lineitems = InvoiceLineitem.objects.filter(invoice=invoice)
                total_basic = 0.0
                grand_total = 0.0

                for item in invoice_lineitems:
                        total_basic = total_basic + item.total_basic_price
                        grand_total = grand_total + item.total_price

                invoice.basic_value = round(total_basic,2)
                invoice.total_value = round(grand_total,2)
                invoice.save()

                return HttpResponseRedirect(reverse('invoice-selected-lineitem',args=[invoice_no]))

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


#Edit _lineitem
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

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/invoice_lineitem_edit.html",context)

        if request.method == 'POST':
                data = request.POST
                item = InvoiceLineitem.objects.get(id = lineitem_id)


                if item.product_title != 'added_by_accounts':
                        item.product_title = data['product_title']
                        item.model = data['model']
                        item.brand = data['brand']
                        item.product_code = data['product_code']
                        item.part_number = data['part_number']

                        igl = InvoiceGRNLink.objects.filter(invoice_lineitem=item)

                        igl_quantity = 0
                        for igl_item in igl:
                                igl_quantity = igl_quantity + igl_item.quantity
                        
                        if float(data['quantity']) > igl_quantity:
                                return JsonResponse({"message" : "Error, Maximum inventory " + str(igl_quantity)})
                
                
                item.description = data['description']
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

#Delete Item
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

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/invoice_lineitem_delete.html",context)

        if request.method == 'POST':
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

#Continue invoice
@login_required(login_url="/employee/login/")
def invoice_continue(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                i = InvoiceTracker.objects.get(invoice_no=invoice_no)

                if i.generating_status == 'creation_in_progress':
                        if i.basic_value <= 0:
                                return(JsonResponse({'Message':'Value should be greater than zero'}))

                        context['billing_address'] = i.cpo.billing_address
                        context['shipping_address'] = i.cpo.shipping_address
                        context['gst_number'] = i.cpo.customer.gst_number
                        context['requester'] = i.cpo.customer_contact_person.name
                        context['requester_ph_no'] = i.cpo.customer_contact_person.mobileNo1
                
                
                        try:
                                context['receiver'] = i.cpo.delivery_contact_person.person_name
                        except:
                                context['receiver'] = 'None'
                
                        try:
                                context['receiver_department'] = i.cpo.delivery_contact_person.department_name
                        except:
                                context['receiver_department'] = 'None'
                
                        try:
                                context['receiver_ph_no'] = i.cpo.delivery_contact_person.mobileNo1
                        except:
                                context['receiver_ph_no'] = 'None'

                
                        context['cpo_no'] = i.cpo.customer_po_no
                        context['cpo_date'] = i.cpo.customer_po_date
                        context['vendor_code'] = i.cpo.customer.vendor_code

                        context['po_document'] = i.cpo.document1
                
                if i.generating_status == 'creation_in_progress_1':

                        context['billing_address'] = i.billing_address
                        context['shipping_address'] = i.shipping_address
                        context['gst_number'] = i.cpo.customer.gst_number
                        context['requester'] = i.requester
                        context['requester_ph_no'] = i.requester_phone_no
                
                
                        context['receiver'] = i.receiver
                        context['receiver_department'] = i.receiver_department
                        context['receiver_ph_no'] = i.receiver_phone_no
                        
                        context['cpo_no'] = i.po_reference
                        context['cpo_date'] = i.po_date
                        context['vendor_code'] = i.cpo.customer.vendor_code

                        context['po_document'] = i.cpo.document1

                context['remarks'] = i.remarks
                context['other_info1'] = i.other_info1
                context['other_info2'] = i.other_info2
                context['other_info3'] = i.other_info3
                context['other_info4'] = i.other_info4
                context['other_info5'] = i.other_info5
                context['other_info6'] = i.other_info6
                context['other_info7'] = i.other_info7


                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/invoice_info_add.html",context)

        if request.method == 'POST':
                data = request.POST

                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                invoice.billing_address = data['billing_address']
                invoice.shipping_address = data['shipping_address']
                invoice.cpo.customer.gst_number = data['gst_number']
                invoice.cpo.customer.vendor_code = data['vendor_code']
                invoice.cpo.customer.save()

                invoice.requester = data['requester']
                invoice.requester_phone_no = data['requester_ph_no']

                invoice.receiver = data['receiver']
                invoice.receiver_department = data['receiver_department']
                invoice.receiver_phone_no = data['receiver_ph_no']

                invoice.remarks = data['remarks']
                invoice.other_info1 = data['other_info_1']
                invoice.other_info2 = data['other_info_2']
                invoice.other_info3 = data['other_info_3']
                invoice.other_info4 = data['other_info_4']
                invoice.other_info5 = data['other_info_5']
                invoice.other_info6 = data['other_info_6']
                invoice.other_info7 = data['other_info_7']

                invoice.generating_status = 'creation_in_progress_1'

                invoice.save()

                context['invoice_no'] = invoice_no
                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/invoice_date_selection.html",context)
                

#Generate Invoice
@login_required(login_url="/employee/login/")
def invoice_generate(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                data = request.POST

                invoice.invoice_date = data['invoice_date']
                invoice.save()

                if invoice.generating_status == 'Generated':
                        cpo_testing_flag = 'Yes'
                        for pending_item in pending_delivery_items :
                                if pending_item.pending_quantity > 0:
                                        cpo_testing_flag = 'No'

                        if cpo_testing_flag == 'Yes':
                                customer_po.status = 'Invoiced_Done'
                                customer_po.save()
                        context['invoice_no'] = invoice_no
                        return render(request,"Accounts/Invoice/get_invoice_copy.html",context)



                customer_po = invoice.cpo

                pending_delivery_items = PendingDelivery.objects.filter(cpo_lineitem__cpo = customer_po)
                invoice_lineitems = InvoiceLineitem.objects.filter(invoice = invoice)
                grn_lineitems = GRNLineitem.objects.filter(cpo_lineitem__cpo = customer_po)


                #Deduct from Pending Delivery
                for pending_item in pending_delivery_items :
                        for invoice_item in invoice_lineitems :
                                if invoice_item.product_title != 'added_by_accounts':
                                        if pending_item.cpo_lineitem == invoice_item.customer_po_lineitem :
                                                pending_item.pending_quantity = pending_item.pending_quantity - invoice_item.quantity

                                                if pending_item.pending_quantity < 0 :
                                                        return JsonResponse({'message' : 'Something wrong in quantity, please check manually and try again'})

                #Deduct from Inventory
                for invoice_item in invoice_lineitems :
                        if invoice_item.product_title != 'added_by_accounts':
                                effective_quantity = invoice_item.quantity

                                for grn_item in grn_lineitems:
                                        if grn_item.cpo_lineitem == invoice_item.customer_po_lineitem:
                                                available_quantity = grn_item.quantity - grn_item.invoiced_quantity
                                                if available_quantity > 0:
                                                        if available_quantity >= effective_quantity:
                                                                grn_item.invoiced_quantity = grn_item.invoiced_quantity + effective_quantity
                                                                effective_quantity = 0
                                                        
                                                        else:
                                                                grn_item.invoiced_quantity = grn_item.invoiced_quantity + available_quantity
                                                                effective_quantity = effective_quantity - available_quantity

                cpo_testing_flag = 'Yes'
                for pending_item in pending_delivery_items :
                        if pending_item.pending_quantity > 0:
                                cpo_testing_flag = 'No'

                if cpo_testing_flag == 'Yes':
                        customer_po.status = 'Invoiced_Done'
                        customer_po.save()


                for pending_item in pending_delivery_items :
                        pending_item.save()
                
                for grn_item in grn_lineitems:
                        grn_item.save()

                

                invoice.generating_status = 'Generated'
                invoice.save()
                Invoice_Generator(invoice_no)

                


                if type == 'Accounts':
                        context['invoice_no'] = invoice_no
                        return render(request,"Accounts/Invoice/get_invoice_copy.html",context)


##-----------------End Invoice based on supplier item received--------------------------


##Invoice based on direct received items
@login_required(login_url="/employee/login/")
def indirect_invoice_item_selection(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                pending_delivery = PendingDelivery.objects.filter(cpo_lineitem__cpo = invoice.cpo).values(
                        'cpo_lineitem__id',
                        'cpo_lineitem__product_title',
                        'cpo_lineitem__description',
                        'cpo_lineitem__model',
                        'cpo_lineitem__brand',
                        'cpo_lineitem__product_code',
                        'cpo_lineitem__part_no',
                        'pending_quantity',
                        'cpo_lineitem__uom'
                )
                context['po_document'] = invoice.cpo.document1
                context['pending_delivery'] = pending_delivery

                selected_items_from_inventory = InvoiceGRNLink.objects.filter(invoice_lineitem__invoice = invoice).values(
                        'id',
                        'grn_lineitem__grn__grn_no',
                        'grn_lineitem__grn__vendor__name',
                        'grn_lineitem__id',
                        'grn_lineitem__product_title',
                        'grn_lineitem__description',
                        'grn_lineitem__model',
                        'grn_lineitem__brand',
                        'quantity',
                        'invoice_lineitem__customer_po_lineitem__id'
                )
                context['selected_items_from_inventory'] = selected_items_from_inventory
                context['invoice_no'] = invoice_no

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Indirect/item_inventory_mapping.html",context)
                
##Invoice select items from Inventory
@login_required(login_url="/employee/login/")
def indirect_invoice_select_item_from_inventory(request,invoice_no=None,cpo_lineitem_id=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                inventory_items = GRNLineitem.objects.all().values(
                        'id',
                        'product_title',
                        'description',
                        'model',
                        'brand',
                        'product_code',
                        'uom',
                        'quantity',
                        'invoiced_quantity',
                        'unit_price',
                        'gst',
                        'grn__grn_no',
                        'grn__date',
                        'grn__vendor__name'
                )
                context['inventory_items'] = inventory_items
                cpo_lineitem = CPOLineitem.objects.get(id= cpo_lineitem_id)
                pending_delivery = PendingDelivery.objects.filter(cpo_lineitem=cpo_lineitem)

                context['description'] = cpo_lineitem.description
                context['product_title'] = cpo_lineitem.product_title
                context['quantity'] = pending_delivery[0].pending_quantity
                context['invoice_no'] = invoice_no
                context['cpo_lineitem_id'] = cpo_lineitem_id
 
                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Indirect/inventory_list.html",context)

##Invoice - inventory choose  quantity
@login_required(login_url="/employee/login/")
def indirect_invoice_inventory_choose_quantity(request,invoice_no=None,cpo_lineitem_id=None,grn_lineitem_id=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                grn_lineitem = GRNLineitem.objects.get(id = grn_lineitem_id)
                cpo_lineitem = CPOLineitem.objects.get(id= cpo_lineitem_id)
                pending_delivery = PendingDelivery.objects.filter(cpo_lineitem=cpo_lineitem)

                context['pending_quantity'] = pending_delivery[0].pending_quantity
                context['available_quantity'] = grn_lineitem.quantity - grn_lineitem.invoiced_quantity

                if float(pending_delivery[0].pending_quantity) < float(grn_lineitem.quantity - grn_lineitem.invoiced_quantity):
                        suggested_quantity = pending_delivery[0].pending_quantity
                else:
                        suggested_quantity = grn_lineitem.quantity - grn_lineitem.invoiced_quantity

                context['suggested_quantity'] = suggested_quantity

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Indirect/put_quantity.html",context)

        if request.method == 'POST':
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                grn_lineitem = GRNLineitem.objects.get(id = grn_lineitem_id)
                cpo_lineitem = CPOLineitem.objects.get(id= cpo_lineitem_id)
                pending_delivery = PendingDelivery.objects.filter(cpo_lineitem=cpo_lineitem)
                
                if float(pending_delivery[0].pending_quantity) < float(grn_lineitem.quantity - grn_lineitem.invoiced_quantity):
                        suggested_quantity = pending_delivery[0].pending_quantity
                else:
                        suggested_quantity = grn_lineitem.quantity - grn_lineitem.invoiced_quantity

                data = request.POST
                
                if float(data['quantity'])==0:
                        return(JsonResponse({'Message':'not allowed'}))

                if float(data['quantity'])>suggested_quantity:
                        return(JsonResponse({'Message':'Quantity exceeding'}))

                
                lineitem_count = InvoiceLineitem.objects.filter(invoice = invoice_no, customer_po_lineitem = cpo_lineitem).count()
                if lineitem_count == 0:
                        invoice_item = InvoiceLineitem.objects.create(
                                invoice = invoice,
                                customer_po_lineitem = cpo_lineitem,
                                product_title = cpo_lineitem.product_title,
                                description = cpo_lineitem.description,
                                model = cpo_lineitem.model,
                                brand = cpo_lineitem.brand,
                                product_code = cpo_lineitem.product_code,
                                part_number = cpo_lineitem.part_no,
                                hsn_code = cpo_lineitem.hsn_code,
                                uom = cpo_lineitem.uom,
                                unit_price = cpo_lineitem.unit_price,
                                gst = cpo_lineitem.gst
                        )
                else:
                        invoice_item = InvoiceLineitem.objects.filter(invoice = invoice_no, customer_po_lineitem = cpo_lineitem)[0]
                        
                        previous_linked_item = InvoiceGRNLink.objects.filter(invoice_lineitem = invoice_item)
                        
                        p_quantity = 0
                        for p_l_item in previous_linked_item:
                                p_quantity = p_quantity + p_l_item.quantity

                        if (p_quantity + float(data['quantity'])) > pending_delivery[0].pending_quantity:
                                return(JsonResponse({'Message':'Quantity exceeding'}))

                InvoiceGRNLink.objects.create(
                        invoice_lineitem = invoice_item,
                        grn_lineitem = grn_lineitem,
                        quantity = float(data['quantity'])
                )
                return HttpResponseRedirect(reverse('indirect-invoice-item-selection',args=[invoice_no]))
                        
#Invoice -- selected inventory item delete
@login_required(login_url="/employee/login/")
def indirect_invoice_inventory_item_delete(request,invoice_no=None,link_id=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                invoice_grn_link = InvoiceGRNLink.objects.get(id = link_id)

                context['product_title'] = invoice_grn_link.grn_lineitem.product_title
                context['quantity'] = invoice_grn_link.quantity

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Indirect/remove_item.html",context)
        
        if request.method == 'POST':
                invoice_grn_link = InvoiceGRNLink.objects.get(id = link_id)
                invoice_grn_link.invoice_lineitem.delete()

                return HttpResponseRedirect(reverse('indirect-invoice-item-selection',args=[invoice_no]))

#Invoice - Show selected item details
@login_required(login_url="/employee/login/")
def indirect_invoice_show_item_details(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                invoice_value_calculation(invoice_no)
                quantity_integrator(invoice_no)
                invoice = InvoiceTracker.objects.get(invoice_no=invoice_no)
                invoice_lineitem = InvoiceLineitem.objects.filter(invoice = invoice)
                context['invoice_lineitem'] = invoice_lineitem
                context['invoice_no'] = invoice_no

                context['invoice_total_basic'] = invoice.basic_value
                context['invoice_total_gst'] = round((invoice.total_value - invoice.basic_value),2)
                context['invoice_total'] = invoice.total_value

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Indirect/invoice_selected_lineitem.html",context)
        
        if request.method == 'POST':
                data = request.POST
                invoice = InvoiceTracker.objects.get(invoice_no=invoice_no)

                total_basic_value = float(data['quantity']) * float(data['unit_price'])
                total_value = total_basic_value + (total_basic_value * float(data['gst']) / 100)

                InvoiceLineitem.objects.create(
                        invoice = invoice,
                        product_title = 'added_by_accounts',
                        description = data['description'],
                        hsn_code = data['hsn_code'],
                        quantity = float(data['quantity']),
                        uom = data['uom'],
                        unit_price = float(data['unit_price']),
                        total_basic_price = round(total_basic_value,2),
                        total_price = round(total_value,2),
                        gst = float(data['gst'])
                )

                invoice_value_calculation(invoice_no)
                return HttpResponseRedirect(reverse('indirect-invoice-show-item-details',args=[invoice_no]))

#Invoice -- continue
@login_required(login_url="/employee/login/")
def indirect_invoice_continue(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                i = InvoiceTracker.objects.get(invoice_no = invoice_no)

                invoice_lineitem_count = InvoiceLineitem.objects.filter(invoice = i).count()

                if invoice_lineitem_count == 0:
                        return(JsonResponse({'message' : 'No Lineitem Found'}))
                
                invoice_value_calculation(invoice_no)

                if i.generating_status == 'creation_in_progress':
                        

                        context['billing_address'] = i.cpo.billing_address
                        context['shipping_address'] = i.cpo.shipping_address
                        context['gst_number'] = i.cpo.customer.gst_number
                        context['requester'] = i.cpo.customer_contact_person.name
                        context['requester_ph_no'] = i.cpo.customer_contact_person.mobileNo1
                
                
                        try:
                                context['receiver'] = i.cpo.delivery_contact_person.person_name
                        except:
                                context['receiver'] = 'None'
                
                        try:
                                context['receiver_department'] = i.cpo.delivery_contact_person.department_name
                        except:
                                context['receiver_department'] = 'None'
                
                        try:
                                context['receiver_ph_no'] = i.cpo.delivery_contact_person.mobileNo1
                        except:
                                context['receiver_ph_no'] = 'None'

                
                        context['cpo_no'] = i.cpo.customer_po_no
                        context['cpo_date'] = i.cpo.customer_po_date
                        context['vendor_code'] = i.cpo.customer.vendor_code

                        context['po_document'] = i.cpo.document1
                
                if i.generating_status == 'creation_in_progress_1':

                        context['billing_address'] = i.billing_address
                        context['shipping_address'] = i.shipping_address
                        context['gst_number'] = i.cpo.customer.gst_number
                        context['requester'] = i.requester
                        context['requester_ph_no'] = i.requester_phone_no
                
                
                        context['receiver'] = i.receiver
                        context['receiver_department'] = i.receiver_department
                        context['receiver_ph_no'] = i.receiver_phone_no
                        
                        context['cpo_no'] = i.po_reference
                        context['cpo_date'] = i.po_date
                        context['vendor_code'] = i.cpo.customer.vendor_code

                        context['po_document'] = i.cpo.document1

                context['remarks'] = i.remarks
                context['other_info1'] = i.other_info1
                context['other_info2'] = i.other_info2
                context['other_info3'] = i.other_info3
                context['other_info4'] = i.other_info4
                context['other_info5'] = i.other_info5
                context['other_info6'] = i.other_info6
                context['other_info7'] = i.other_info7


                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Indirect/invoice_info_add.html",context)

        if request.method == 'POST':
                data = request.POST

                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                invoice.billing_address = data['billing_address']
                invoice.shipping_address = data['shipping_address']
                invoice.cpo.customer.gst_number = data['gst_number']
                invoice.cpo.customer.vendor_code = data['vendor_code']
                invoice.cpo.customer.save()

                invoice.requester = data['requester']
                invoice.requester_phone_no = data['requester_ph_no']

                invoice.receiver = data['receiver']
                invoice.receiver_department = data['receiver_department']
                invoice.receiver_phone_no = data['receiver_ph_no']

                invoice.remarks = data['remarks']
                invoice.other_info1 = data['other_info_1']
                invoice.other_info2 = data['other_info_2']
                invoice.other_info3 = data['other_info_3']
                invoice.other_info4 = data['other_info_4']
                invoice.other_info5 = data['other_info_5']
                invoice.other_info6 = data['other_info_6']
                invoice.other_info7 = data['other_info_7']

                invoice.generating_status = 'creation_in_progress_1'

                invoice.save()

                context['invoice_no'] = invoice_no
                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Indirect/invoice_date_selection.html",context)

#Indirect invoice delete
@login_required(login_url="/employee/login/")
def indirect_invoice_delete(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                
                if invoice.generating_status == 'creation_in_progress':
                        invoice.delete()
                
                elif invoice.generating_status == 'creation_in_progress_1':
                        invoice.delete()
                
                else:
                        return JsonResponse({'message':'delete not possible'})

                return HttpResponseRedirect(reverse('invoice-creation-purchase-order-selection'))

#Indirect Generate Invoice
@login_required(login_url="/employee/login/")
def indirect_invoice_generate(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                data = request.POST

                invoice.invoice_date = data['invoice_date']
                invoice.save()

                if invoice.generating_status == 'Generated':
                        Invoice_Generator(invoice_no)
                        context['invoice_no'] = invoice_no
                        return render(request,"Accounts/Invoice/get_invoice_copy.html",context)



                customer_po = invoice.cpo

                pending_delivery_items = PendingDelivery.objects.filter(cpo_lineitem__cpo = customer_po)
                invoice_lineitems = InvoiceLineitem.objects.filter(invoice = invoice)
                #grn_lineitems = GRNLineitem.objects.filter(cpo_lineitem__cpo = customer_po)
                grn_linkitems = InvoiceGRNLink.objects.filter(invoice_lineitem__invoice = invoice)


                #Deduct from Pending Delivery
                for pending_item in pending_delivery_items :
                        for invoice_item in invoice_lineitems :
                                if invoice_item.product_title != 'added_by_accounts':
                                        if pending_item.cpo_lineitem == invoice_item.customer_po_lineitem :
                                                pending_item.pending_quantity = round((pending_item.pending_quantity - invoice_item.quantity),2)

                                                if pending_item.pending_quantity < 0 :
                                                        return JsonResponse({'message' : 'Something wrong in quantity, please check manually and try again'})

                #Deduct from Inventory
                for item in grn_linkitems:
                        item.grn_lineitem.invoiced_quantity = round((item.grn_lineitem.invoiced_quantity + item.quantity),2)
                        if item.grn_lineitem.quantity < item.grn_lineitem.invoiced_quantity:
                                return JsonResponse({'message' : 'Something wrong in quantity, please check manually and try again'})
                
                for item in grn_linkitems:        
                        item.grn_lineitem.save()
                
                cpo_testing_flag = 'Yes'
                for pending_item in pending_delivery_items :
                        if pending_item.pending_quantity > 0:
                                cpo_testing_flag = 'No'

                if cpo_testing_flag == 'Yes':
                        customer_po.status = 'Invoiced_Done'
                        customer_po.save()


                for pending_item in pending_delivery_items :
                        pending_item.save()
                

                

                invoice.generating_status = 'Generated'
                invoice.save()
                Invoice_Generator(invoice_no)

                


                if type == 'Accounts':
                        context['invoice_no'] = invoice_no
                        return render(request,"Accounts/Invoice/Indirect/get_invoice_copy.html",context)


def invoice_value_calculation(invoice_no):
        invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
        invoice_lineitem = InvoiceLineitem.objects.filter(invoice = invoice)

        invoice_basic_value = 0
        invoice_total_value = 0

        for item in invoice_lineitem:
                item.total_basic_price = round((float(item.unit_price) * float(item.quantity)), 2)
                item.total_price = round((item.total_basic_price + (item.total_basic_price * float(item.gst) / 100)), 2)

                item.save()
                invoice_basic_value = invoice_basic_value + item.total_basic_price
                invoice_total_value = invoice_total_value + item.total_price

        invoice.basic_value = invoice_basic_value
        invoice.total_value = invoice_total_value
        invoice.save()

def quantity_integrator(invoice_no):
        invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)

        invoice_lineitems = InvoiceLineitem.objects.filter(invoice = invoice)
        invoice_link = InvoiceGRNLink.objects.filter(invoice_lineitem__invoice = invoice)
        
        for item in invoice_lineitems:
                quantity = 0
                for link_item in invoice_link:
                        if link_item.invoice_lineitem == item:
                                quantity = quantity + link_item.quantity
                
                item.quantity = quantity
                item.save()

##-------------------------------------------Direct Invoice------------------------------

#Customer Selection
@login_required(login_url="/employee/login/")
def direct_invoice_customer_selection(request):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                processing_count = InvoiceTracker.objects.filter(Q(generating_status='creation_in_progress') | Q(generating_status='creation_in_progress_1')).count()

                if processing_count > 0:
                        processing_invoice_list = InvoiceTracker.objects.filter(Q(generating_status='creation_in_progress') | Q(generating_status='creation_in_progress_1'))
                        context['processing_invoicce_list'] = processing_invoice_list
                        return render(request,"Accounts/Invoice/invoice_processing_list.html",context)


                customer_list = CustomerProfile.objects.all().values(
                        'id',
                        'name',
                        'location',
                        'code',
                        'state',
                        'tax_type'
                )
                context['customer_list'] = customer_list
                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Direct/customer_selection.html",context)

    
#Customer COntact Person Selection
@login_required(login_url="/employee/login/")
def direct_invoice_customer_contact_person_selection(request, customer_id = None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == "GET":
                ContactPerson = CustomerContactPerson.objects.filter(customer_name__pk=customer_id)
                context['ContactPerson'] = ContactPerson
                customer = CustomerProfile.objects.get(id=customer_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = customer_id

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Direct/contact_person_selection.html",context)

        if request.method == "POST":
                data = request.POST
                customer = CustomerProfile.objects.get(id=customer_id)
                contactperson_id =  customer_id +'P' + str(CustomerContactPerson.objects.count() + 1)
                cp = CustomerContactPerson.objects.create(id=contactperson_id,name=data['name'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],customer_name=customer,created_by=u)
                if cp:
                        context['message'] = 'Successfully registered ' + data['name']
                        context['message_type'] = 'success'
                else:
                        context['message'] = 'Something went wrong'
                        context['message_type'] = 'danger'
      
                ContactPerson = CustomerContactPerson.objects.filter(customer_name__pk=customer_id)
                context['ContactPerson'] = ContactPerson
                customer = CustomerProfile.objects.get(id=customer_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = customer_id
                
                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Direct/contact_person_selection.html",context)

#Customer Receiver Selection
@login_required(login_url="/employee/login/")
def direct_invoice_receiver_selection(request, customer_id = None, contact_person_id = None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == "GET":
                receiver = DeliveryContactPerson.objects.filter(customer_name__pk=customer_id)
                context['receiver'] = receiver
                customer = CustomerProfile.objects.get(id=customer_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = customer_id
                context['ContactPersonID'] = contact_person_id

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Direct/receiver_selection.html",context)

        if request.method == "POST":
                data = request.POST
                customer = CustomerProfile.objects.get(id=customer_id)
                enduser_id =  customer_id +'D' + str(DeliveryContactPerson.objects.count() + 1)
                cp = DeliveryContactPerson.objects.create(id=enduser_id,person_name=data['name'],department_name = data['dept'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],customer_name=customer,created_by=u)
                if cp:
                        context['message'] = 'Successfully registered ' + data['name']
                        context['message_type'] = 'success'
                else:
                        context['message'] = 'Something went wrong'
                        context['message_type'] = 'danger'

                context['login_user_name'] = u.first_name + ' ' + u.last_name
                receiver = DeliveryContactPerson.objects.filter(customer_name__pk=customer_id)
                context['receiver'] = receiver
                customer = CustomerProfile.objects.get(id=customer_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = customer_id
                context['ContactPersonID'] = contact_person_id
        
                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Direct/receiver_selection.html",context)


#Direct Invoice- invoice Number Generate
@login_required(login_url="/employee/login/")
def direct_invoice_number_generate(request, customer_id = None, contact_person_id = None, delivery_contact_person_id = None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                processing_count = InvoiceTracker.objects.filter(Q(generating_status='creation_in_progress') | Q(generating_status='creation_in_progress_1')).count()

                if processing_count > 0:
                        return(JsonResponse({'message' : 'please complete previous invoice'}))

                financial_year = get_financial_year(datetime.datetime.today().strftime('%Y-%m-%d'))
                invoice_count = (InvoiceTracker.objects.filter(financial_year = financial_year).count()) + 1
                invoice_no = 'AP' + financial_year + "{:04d}".format(invoice_count)
                print(invoice_no)

                customer = CustomerProfile.objects.get(id = customer_id)
                contact_person = CustomerContactPerson.objects.get(id = contact_person_id)
                
                invoice_obj = InvoiceTracker.objects.create(
                        invoice_no = invoice_no,
                        customer = customer,
                        customer_contact_person = contact_person,
                        requester = contact_person.name,
                        requester_phone_no = contact_person.mobileNo1,
                        billing_address = customer.billing_address,
                        shipping_address = customer.shipping_address,
                        financial_year = financial_year
                )

                return HttpResponseRedirect(reverse('direct-invoice-lineitem-selection',args=[invoice_no]))
                

#Direct Invoice- lineitem_selection
@login_required(login_url="/employee/login/")
def direct_invoice_lineitem_selection(request, invoice_no = None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)

                invoice_lineitem = InvoiceLineitem.objects.filter(invoice = invoice).values(
                        'id',
                        'product_title',
                        'description',
                        'model',
                        'brand',
                        'product_code',
                        'part_number',
                        'hsn_code',
                        'quantity',
                        'uom',
                        'unit_price',
                        'total_basic_price',
                        'gst',
                        'total_price'
                )
                context['invoice_lineitem'] = invoice_lineitem
                context['invoice'] = invoice
                context['invoice_no'] = invoice_no
                
                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Direct/invoice_selected_lineitem.html",context)

        if request.method == 'POST':
                data = request.POST
                invoice = InvoiceTracker.objects.get(invoice_no=invoice_no)

                total_basic_value = float(data['quantity']) * float(data['unit_price'])
                total_value = total_basic_value + (total_basic_value * float(data['gst']) / 100)

                InvoiceLineitem.objects.create(
                        invoice = invoice,
                        product_title = 'added_by_accounts',
                        description = data['description'],
                        model = data['model'],
                        brand = data['brand'],
                        product_code = data['product_code'],
                        part_number = data['part_no'],
                        hsn_code = data['hsn_code'],
                        quantity = float(data['quantity']),
                        uom = data['uom'],
                        unit_price = float(data['unit_price']),
                        total_basic_price = round(total_basic_value,2),
                        total_price = round(total_value,2),
                        gst = float(data['gst'])
                )
                invoice_value_calculation(invoice_no)
                return HttpResponseRedirect(reverse('direct-invoice-lineitem-selection',args=[invoice_no]))

#Direct Invoice- lineitem delete
@login_required(login_url="/employee/login/")
def direct_invoice_lineitem_delete(request, invoice_no = None, lineitem_id = None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name        

        if request.method == 'GET':
                item = InvoiceLineitem.objects.get(id = lineitem_id)
                context['item'] = item

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Direct/invoice_lineitem_delete.html",context)

        if request.method == 'POST':
                invoice_lineitem = InvoiceLineitem.objects.get(id = lineitem_id)
                invoice_lineitem.delete()
                invoice_value_calculation(invoice_no)

                return HttpResponseRedirect(reverse('direct-invoice-lineitem-selection',args=[invoice_no]))

#Direct Invoice- lineitem edit
@login_required(login_url="/employee/login/")
def direct_invoice_lineitem_edit(request, invoice_no = None, lineitem_id = None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name        

        if request.method == 'GET':
                item = InvoiceLineitem.objects.get(id = lineitem_id)
                context['item'] = item

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Direct/invoice_lineitem_edit.html",context) 

        if request.method == 'POST':
                data = request.POST

                lnvoice_lineitem = InvoiceLineitem.objects.get(id = lineitem_id)
                
                lnvoice_lineitem.description = data['description']
                lnvoice_lineitem.model = data['model']
                lnvoice_lineitem.brand = data['brand']
                lnvoice_lineitem.product_code = data['product_code']
                lnvoice_lineitem.part_number = data['part_number']
                lnvoice_lineitem.hsn_code = data['hsn_code']
                lnvoice_lineitem.quantity = float(data['quantity'])
                lnvoice_lineitem.uom = data['uom']
                lnvoice_lineitem.unit_price = float(data['unit_price'])
                lnvoice_lineitem.gst = float(data['gst'])

                lnvoice_lineitem.save()

                invoice_value_calculation(invoice_no)
                return HttpResponseRedirect(reverse('direct-invoice-lineitem-selection',args=[invoice_no]))

#Continue invoice
@login_required(login_url="/employee/login/")
def direct_invoice_continue(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                i = InvoiceTracker.objects.get(invoice_no=invoice_no)

                context['billing_address'] = i.billing_address
                context['shipping_address'] = i.shipping_address
                context['gst_number'] = i.customer.gst_number
                context['requester'] = i.requester
                context['requester_ph_no'] = i.requester_phone_no
                
                
                context['receiver'] = i.receiver
                context['receiver_department'] = i.receiver_department
                context['receiver_ph_no'] = i.receiver_phone_no
                        
                context['cpo_no'] = i.po_reference
                context['cpo_date'] = i.po_date
                context['vendor_code'] = i.customer.vendor_code


                context['remarks'] = i.remarks
                context['other_info1'] = i.other_info1
                context['other_info2'] = i.other_info2
                context['other_info3'] = i.other_info3
                context['other_info4'] = i.other_info4
                context['other_info5'] = i.other_info5
                context['other_info6'] = i.other_info6
                context['other_info7'] = i.other_info7


                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Direct/invoice_info_add.html",context)

        if request.method == 'POST':
                data = request.POST

                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                invoice.billing_address = data['billing_address']
                invoice.shipping_address = data['shipping_address']
                invoice.customer.gst_number = data['gst_number']
                invoice.customer.vendor_code = data['vendor_code']
                invoice.customer.save()

                invoice.requester = data['requester']
                invoice.requester_phone_no = data['requester_ph_no']

                invoice.receiver = data['receiver']
                invoice.receiver_department = data['receiver_department']
                invoice.receiver_phone_no = data['receiver_ph_no']

                invoice.remarks = data['remarks']
                invoice.other_info1 = data['other_info_1']
                invoice.other_info2 = data['other_info_2']
                invoice.other_info3 = data['other_info_3']
                invoice.other_info4 = data['other_info_4']
                invoice.other_info5 = data['other_info_5']
                invoice.other_info6 = data['other_info_6']
                invoice.other_info7 = data['other_info_7']

                invoice.generating_status = 'creation_in_progress_1'

                invoice.save()

                context['invoice_no'] = invoice_no
                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/Direct/invoice_date_selection.html",context)

#Direct Generate Invoice
@login_required(login_url="/employee/login/")
def direct_invoice_generate(request,invoice_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                data = request.POST

                invoice.invoice_date = data['invoice_date']            
                
                invoice.generating_status = 'Generated'
                invoice.save()
                Invoice_Generator(invoice_no)

                if type == 'Accounts':
                        context['invoice_no'] = invoice_no
                        return render(request,"Accounts/Invoice/Direct/get_invoice_copy.html",context)


#-----------------------------------------------------Manage Invoices-------------------------------------------------------------
#Invoice List
@login_required(login_url="/employee/login/")
def invoice_list(request):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                invoice_list = InvoiceTracker.objects.all().values(
                        'invoice_no',
                        'invoice_date',
                        'customer__name',
                        'customer__location',
                        'po_reference',
                        'po_date',
                        'basic_value',
                        'total_value',
                        'generating_status'
                )
                context['invoice_list'] = invoice_list

                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/ManageInvoice/invoice_list.html",context)

#Invoice Lineitems
@login_required(login_url="/employee/login/")
def invoice_lineitems(request,invoice_no = None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                invoice_lineitems = InvoiceLineitem.objects.filter(invoice = invoice).values(
                        'id',
                        'product_title',
                        'description',
                        'model',
                        'brand',
                        'product_code',
                        'part_number',
                        'hsn_code',
                        'quantity',
                        'uom',
                        'unit_price',
                        'total_basic_price',
                        'gst',
                        'total_price'
                )

                context['invoice_lineitem'] = invoice_lineitems
                context['invoice'] = invoice
                context['invoice_no'] = invoice_no
                
                if type == 'Accounts':
                        return render(request,"Accounts/Invoice/ManageInvoice/invoice_selected_lineitem.html",context)


##-------------------------------Generate Invoice-----------------------------------------------------------
def Invoice_Generator(invoice_no):  
        #Extract Invoice Data
        invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
        invoice_lineitems = InvoiceLineitem.objects.filter(invoice = invoice)
        pdf = canvas.Canvas("media/invoice/" + invoice_no + ".pdf", pagesize=A4)
        pdf.setTitle(invoice_no + '.pdf')
        pdf.showPage()
        pdf.save()