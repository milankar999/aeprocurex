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
from num2words import num2words



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

                cpo_list = CustomerPO.objects.filter(Q(status = 'po_processed') | Q(status = 'Full_Product_Received') | Q(status = 'direct_processing') | Q(status = 'approved')).values(
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
                if(not(invoice.customer.bank_account)):
                        return JsonResponse({'message':'bank details not found'})
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
                inventory_items = GRNLineitem.objects.filter(~Q(grn__status = 'deleted')).values(
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
                if(not(invoice.customer.bank_account)):
                        return JsonResponse({'message':'bank details not found'})
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
                if(not(invoice.customer.bank_account)):
                        return JsonResponse({'message':'bank details not found'})
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
        tax_type = invoice.customer.tax_type
        state = invoice.customer.state
        Add_Header(pdf, tax_type)
        Add_Footer(pdf)
        invoice_information(
                pdf,
                invoice.invoice_no,
                invoice.invoice_date,
                invoice.po_reference,
                invoice.po_date,
                invoice.customer.vendor_code
        )
        y = Add_To(
                pdf,
                invoice.billing_address,
                invoice.shipping_address,
                invoice.customer.gst_number,
                invoice.requester,
                invoice.requester_phone_no,
                invoice.receiver,
                invoice.receiver_department,
                invoice.receiver_phone_no
        )
        y = Add_Table_Header(pdf, y, state)
        
        i = 1
        for item in invoice_lineitems:
                y = add_lineitem(
                        pdf,
                        y,
                        i,
                        invoice_no,
                        item.product_title,
                        item.description,
                        item.model,
                        item.brand,
                        item.product_code,
                        item.hsn_code,
                        item.quantity,
                        item.uom,
                        item.unit_price,
                        item.total_basic_price,
                        item.gst,
                        item.total_price,
                        tax_type,
                        state
                )
                i = i + 1
        y = add_total(pdf,y,invoice_no,state,tax_type,invoice.basic_value,invoice.total_value)
        if tax_type == 'SEZ':
                words = num2words('{0:.2f}'.format(invoice.basic_value))
        else:
                words = num2words('{0:.2f}'.format(invoice.total_value))
        y = add_amount_in_word(pdf, y,invoice_no,'Rupees In Words : ' + words.title() + ' only',tax_type)
        y = add_bank_details(
                pdf,
                y,
                invoice_no,
                tax_type,
                invoice.customer.bank_account.bank_name,
                invoice.customer.bank_account.account_holder,
                invoice.customer.bank_account.account_number,
                invoice.customer.bank_account.ifcs_code,
                invoice.customer.bank_account.account_type
        )
        y = add_tc(pdf,y,invoice_no,tax_type)
        y = add_other_info(
                pdf,
                y,
                invoice_no,
                tax_type,
                invoice.remarks,
                invoice.other_info1,
                invoice.other_info2,
                invoice.other_info3,
                invoice.other_info4,
                invoice.other_info5,
                invoice.other_info6,
                invoice.other_info7
        )
        pdf.showPage()
        pdf.save()

#Add Front Page Header
def Add_Header(pdf, tax_type):
        print(tax_type)

        if tax_type == 'SEZ':
                pdf.setFont('Helvetica-Bold', 9)
                pdf.drawString(20,820,"SUPPLY  MENT FOR EXPORT / SUPPLY TO SEZ UNIT OR SEZ DEVELOPER FOR AUTHORIZED OPERATIONS  UNDER BOND OR")
                pdf.drawString(160,810,"LETTER OF UNDERTAKING WITHOUT PAYMENT OF GST")
                pdf.drawInlineImage("static/image/aeprocurex.jpg",360,735,220,70)
        else:
                pdf.drawInlineImage("static/image/aeprocurex.jpg",360,750,220,70)
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawString(20,763,"AEPROCUREX SOURCING PRIVATE LIMITED")

        pdf.setFont('Helvetica',9)
        #pdf.setFillColor(HexColor('#000000'))
        pdf.drawString(20,752,"Regd. Office: Shankarappa Complex, No.4")
        pdf.drawString(20,741,"Hosapalya Main Road, Opp. To Om Shakti Temple")
        pdf.drawString(20,730,"HSR Layout Extension,Bangalore - 560068")

        pdf.drawString(20,719,"Telephone: 080-43743-314 / 315")
        pdf.drawString(20,708,"E-mail: sales.p@aeprocurex.com")
        pdf.drawString(20,697,"GST No. 29AAQCA2809L1Z6")
        pdf.drawString(20,686,"PAN No. - AAQCA2809L")
        pdf.drawString(20,675,"CIN No.-U74999KA2017PTC108349")
        if tax_type == 'SEZ':
                pdf.drawString(20,665,"LUT Number : AD290519001230F / 13-May-2019")


        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawString(300,720,"TAX INVOICE")
        #pdf.setFillColor(yellow)
        pdf.rect(300,716,275,1, stroke=1, fill=1)

#Add Footer 
def Add_Footer(pdf):
    pdf.setFont('Helvetica-Bold', 8)
    pdf.rect(20,35,560,1, stroke=1, fill=1)
    pdf.drawString(212,25,'SUBJECT TO BENGALURU JURISDICTION')
    pdf.setFont('Helvetica', 8)
    pdf.drawString(209,15,'This is a Aeprocurex System Generated Invoice')
    pdf.drawString(525,15,'Page-No : ' + str(pdf.getPageNumber()))

#Add Invoice Information
def invoice_information(pdf,invoice_no,invoice_date,order_reference,order_date,vendor_code):
        if vendor_code == None:
                vendor_code = ' '

        pdf.setFont('Helvetica', 9)
        pdf.drawString(300,700,"Invoice No :")
        pdf.drawString(300,688,"Invoice Date :")
       
        pdf.drawString(300,672,"Order Reference :")
        pdf.drawString(300,660,"Order Date :")
        pdf.drawString(300,648,"Vendor Code :")

        pdf.setFont('Helvetica-Bold', 9)
        try:
                pdf.drawString(390,700,invoice_no)
        except:
                pdf.drawString(390,700,"")
        try:
                pdf.drawString(390,688,str(invoice_date.strftime('%d, %b %Y')))
        except:
                pdf.drawString(390,688,"")
        
        
        try:
                pdf.drawString(390,672,order_reference)
        except:
                pdf.drawString(390,672,"")
        try:
                pdf.drawString(390,660,str(order_date.strftime('%d, %b %Y')))
        except:
                pdf.drawString(390,660,"")
        try:
                pdf.drawString(390,648,vendor_code)
        except:
                pdf.drawString(390,648,"")

#Add PO To
def Add_To(pdf,billing_address,shipping_address,gst_number,requester,requester_ph_no,receiver,receiver_department,receiver_phone_no):
        pdf.setFont('Helvetica-Bold', 9)
        pdf.drawString(20,635,'BILL TO')
        
        pdf.setFont('Helvetica', 9)
        wrapper = textwrap.TextWrapper(width=130) 
        word_list = wrapper.wrap(text=billing_address)
        y = 623
        for element in word_list:
                pdf.drawString(20,y,element)
                y = y - 13
        y = y -2
        try:
                pdf.drawString(20,y,'GST # :' + gst_number)
                y = y - 13
        except:
                pass
        y = y - 3

        pdf.setFont('Helvetica-Bold', 9)
        pdf.setFillColor(HexColor('#000000'))
        pdf.drawString(20,y,'SHIP TO')
        y = y - 11
        wrapper = textwrap.TextWrapper(width=130)
        word_list = wrapper.wrap(text=shipping_address)
        pdf.setFont('Helvetica', 9)
        for element in word_list:
                pdf.drawString(20,y,element)
                y = y - 11

        y = y - 3

        ##Requester Data
        req = ''
        if requester != '' and requester != 'None':
                req = req + 'Requester : ' + requester

                if requester_ph_no != '' and receiver_phone_no != 'None':
                        req = req +' ,' + requester_ph_no
        
                if req != '':
                        pdf.setFont('Helvetica-Bold', 8)
                        pdf.setFillColor(HexColor('#000000'))
                        pdf.drawString(20,y,req)
                        y = y -11

        #Receiver Data
        rec = ''
        if receiver != '' and receiver != 'None':
                rec = 'Receiver : ' + receiver

                if receiver_department != '' and receiver_department != 'None':
                        rec = rec + ', Dep : ' + receiver_department

                if receiver_phone_no != '' and receiver_phone_no != 'None':
                        rec = rec + ' ,' + receiver_phone_no

                if req != '':
                        pdf.setFont('Helvetica-Bold', 8)
                        pdf.setFillColor(HexColor('#000000'))
                        pdf.drawString(20,y,rec)
                        y = y -11


        
        return(y)

#Add Table Header
def Add_Table_Header(pdf,y,state):
        if state == 'Karnataka':
                pdf.rect(20,y,560,1, stroke=1, fill=1)
                pdf.setFillColor(HexColor('#E4E4E4'))
                pdf.rect(20,y-31,560,30, stroke=0, fill=1)
                #Colum headers
                pdf.setFillColor(HexColor('#000000'))
                pdf.setFont('Helvetica-Bold', 7)
                pdf.drawString(22,y-17,'SL #')
                pdf.drawString(60,y-17,'Material / Description / Specification')
                pdf.drawString(225,y-17,'Quantity')
                pdf.drawString(275,y-17,'UOM')
                pdf.drawString(310,y-11,'Unit Price')
                pdf.drawString(320,y-22,'(INR) ')
                pdf.drawString(365,y-11,'Total Basic')
                pdf.drawString(365,y-22,'Price (INR)')
                pdf.drawString(420,y-11,'CGST(%)')
                pdf.drawString(428,y-22,'INR')
                pdf.drawString(470,y-11,'SGST(%)')
                pdf.drawString(478,y-22,'INR')
                pdf.drawString(530,y-11,'Total Price')
                pdf.drawString(542,y-22,'(INR)')
                y = y - 31
                pdf.rect(20,y,560,0.1, stroke=1, fill=1)
                y = y - 10
                return(y)

        else:
                pdf.rect(20,y,560,1, stroke=1, fill=1)
                pdf.setFillColor(HexColor('#E4E4E4'))
                pdf.rect(20,y-31,560,30, stroke=0, fill=1)
                #Colum headers
                pdf.setFillColor(HexColor('#000000'))
                pdf.setFont('Helvetica-Bold', 7)
                pdf.drawString(22,y-17,'SL #')
                pdf.drawString(60,y-17,'Material / Description / Specification')
                pdf.drawString(230,y-17,'Quantity')
                pdf.drawString(280,y-17,'UOM')
                pdf.drawString(325,y-11,'Unit Price')
                pdf.drawString(335,y-22,'(INR) ')
                pdf.drawString(380,y-11,'Total Basic')
                pdf.drawString(380,y-22,'Price (INR)')
                pdf.drawString(450,y-11,'IGST(%)')
                pdf.drawString(458,y-22,'INR')
                pdf.drawString(510,y-11,'Total Price')
                pdf.drawString(522,y-22,'(INR)')
                y = y - 31
                pdf.rect(20,y,560,0.1, stroke=1, fill=1)
                y = y - 10
                return(y)

#Add New Page
def add_new_page(pdf,invoice_no,tax_type):
        pdf.setFont('Helvetica-Bold', 8)
        pdf.drawString(534,38,'continued...')

        pdf.showPage()
        print(tax_type)
        if tax_type == 'SEZ':
                pdf.setFont('Helvetica-Bold', 9)
                pdf.drawString(20,820,"SUPPLY  MENT FOR EXPORT / SUPPLY TO SEZ UNIT OR SEZ DEVELOPER FOR AUTHORIZED OPERATIONS  UNDER BOND OR")
                pdf.drawString(160,810,"LETTER OF UNDERTAKING WITHOUT PAYMENT OF GST")
                pdf.drawInlineImage("static/image/aeprocurex.jpg",360,735,220,70)
                pdf.setFont('Helvetica-Bold', 13)
                pdf.drawString(20,750,'INVOICE NO : ' + invoice_no)
                pdf.line(20,740,580,740)
                Add_Footer(pdf)
                return(725)
        else:
                pdf.drawInlineImage("static/image/aeprocurex.jpg",360,750,220,70) 
                pdf.setFont('Helvetica-Bold', 13)
                pdf.drawString(20,763,'INVOICE NO : ' + invoice_no)
                pdf.line(20,748,580,748)
                Add_Footer(pdf)
                return(740)

def currencyInIndiaFormat(n):
        s = n
        l = len(s)
        i = l-1
        res = ''
        flag = 0
        k = 0
        while i>=0:
                if flag==0:
                        res = res + s[i]
                        if s[i]=='.':
                                flag = 1
                elif flag==1:
                        k = k + 1
                        res = res + s[i]
                        if k==3 and i-1>=0:
                                res = res + ','
                                flag = 2
                                k = 0
                else:
                        k = k + 1
                        res = res + s[i]
                        if k==2 and i-1>=0:
                                res = res + ','
                                flag = 2
                                k = 0
                i = i - 1

        return res[::-1]

#Add Lineitem
def add_lineitem(pdf,y,i,invoice_no,product_title,description,model,brand,product_code,hsn_code,quantity,uom,unit_price,total_basic_price,gst,total_price,tax_type,state):
        pdf.setFont('Helvetica', 8)

        item_description = ''

        if description != '' and description != 'None':
                item_description = item_description + ', ' + description

        if model != '' and model != 'None':
                item_description = item_description + ', ' + model
        
        if product_code != '' and product_code != 'None':
                item_description = item_description + ', ' + product_code

        if brand != '' and brand != 'None':
                item_description = item_description + ', ' + brand
        
        #if hsn_code != 'None' and hsn_code != '':
        #        item_description = item_description + ', HSN Code : ' + hsn_code

        if product_title == 'added_by_accounts':
                product_title = ''


        print(item_description)
        if state == 'Karnataka':
                pdf.drawString(22,y,str(i))

                material_wrapper = textwrap.TextWrapper(width=45)
                title_word_list = material_wrapper.wrap(product_title)

                for element in title_word_list:
                        pdf.drawString(50,y,element)
                        break

                pdf.drawString(225,y,'{0:.2f}'.format(quantity))
                pdf.drawString(275,y,str(uom))
                pdf.drawString(310,y,currencyInIndiaFormat('{0:.2f}'.format(unit_price)))
                pdf.drawString(365,y,currencyInIndiaFormat('{0:.2f}'.format(total_basic_price)))
                if tax_type == 'SEZ':
                        pdf.drawString(420,y,'0.00 %')
                        pdf.drawString(470,y,'0.00 %')
                        pdf.drawString(520,y,currencyInIndiaFormat('{0:.2f}'.format(total_basic_price)))
                else:
                        pdf.drawString(420,y,currencyInIndiaFormat('{0:.2f}'.format(round((gst/2),2))+' %'))
                        pdf.drawString(470,y,currencyInIndiaFormat('{0:.2f}'.format(round((gst/2),2))+' %'))
                        pdf.drawString(520,y,currencyInIndiaFormat('{0:.2f}'.format(total_price)))

                material_wrapper = textwrap.TextWrapper(width=45)
                description_word_list = material_wrapper.wrap(item_description)
                flag = 0
                y = y - 11

                for element in description_word_list:
                        #Page Break
                        if flag == 1:
                                if y < 50:
                                        y = add_new_page(pdf,invoice_no,tax_type)
                                        y = Add_Table_Header(pdf,y,state)
                                        pdf.setFont('Helvetica', 8)

                        pdf.drawString(50,y,element)
                        if flag == 0:
                                flag = 1
                                
                                if tax_type == 'SEZ':
                                        pdf.drawString(420,y-2,'0.00')
                                        pdf.drawString(470,y-2,'0.00')
                                else:
                                        cgst = round(((total_price - total_basic_price)/2),2)
                                        sgst = round(((total_price - total_basic_price)/2),2)
                                        
                                        pdf.drawString(420,y-2,currencyInIndiaFormat('{0:.2f}'.format(cgst)))
                                        pdf.drawString(470,y-2,currencyInIndiaFormat('{0:.2f}'.format(sgst)))
                        
                        y = y - 11
                pdf.drawString(50,y,'HSN Code : ' + hsn_code)
                y = y - 5
                pdf.rect(20,y,560, 0.1, stroke=1, fill=1)
  
        else:
                pdf.drawString(22,y,str(i))

                material_wrapper = textwrap.TextWrapper(width=45)
                title_word_list = material_wrapper.wrap(product_title)

                for element in title_word_list:
                        pdf.drawString(50,y,element)
                        break

                pdf.drawString(230,y,'{0:.2f}'.format(quantity))
                pdf.drawString(280,y,str(uom))
                pdf.drawString(325,y,currencyInIndiaFormat('{0:.2f}'.format(unit_price)))
                pdf.drawString(380,y,currencyInIndiaFormat('{0:.2f}'.format(total_basic_price)))
                if tax_type == 'SEZ':
                        pdf.drawString(450,y,'0.00 %')
                        pdf.drawString(510,y,currencyInIndiaFormat('{0:.2f}'.format(total_basic_price)))
                else:
                        pdf.drawString(450,y,currencyInIndiaFormat('{0:.2f}'.format(gst)+' %'))
                        pdf.drawString(510,y,currencyInIndiaFormat('{0:.2f}'.format(total_price)))

                material_wrapper = textwrap.TextWrapper(width=45)
                description_word_list = material_wrapper.wrap(item_description)
                flag = 0
                y = y - 11

                for element in description_word_list:
                        #Page Break
                        if flag == 1:
                                if y < 50:
                                        y = add_new_page(pdf,invoice_no,tax_type)
                                        y = Add_Table_Header(pdf,y,state)
                                        pdf.setFont('Helvetica', 8)

                        pdf.drawString(50,y,element)
                        if flag == 0:
                                flag = 1
                                
                                if tax_type == 'SEZ':
                                        pdf.drawString(450,y-2,'0.00')
                                else:
                                        igst = round((total_price - total_basic_price),2)
                                        pdf.drawString(450,y-2,currencyInIndiaFormat('{0:.2f}'.format(igst)))
                        
                        y = y - 11
                
                pdf.drawString(50,y,'HSN Code : ' + hsn_code)
                y = y - 5     
                pdf.rect(20,y,560, 0.1, stroke=1, fill=1)

        y = y - 9 
        return(y)

#Add total
def add_total(pdf,y,invoice_no,state,tax_type,basic_value,total_value):
        if y < 70:
                y = add_new_page(pdf,invoice_no,tax_type)
        if state == 'Karnataka':
                pdf.rect(300,y,280,1, stroke=1, fill=1)
                pdf.setFillColor(HexColor('#E4E4E4'))
                pdf.rect(300,y-15,280,15, stroke=0, fill=1)
                #Colum headers
                pdf.setFillColor(HexColor('#000000'))
                pdf.setFont('Helvetica-Bold', 7)
                
                pdf.drawString(305,y-11,'Total Basic Value')

                pdf.drawString(390,y-11,'Total CGST')
                pdf.drawString(450,y-11,'Total SGST')
                pdf.drawString(510,y-11,'Grand Total')
                y = y - 15
                pdf.rect(300,y,280,0.1, stroke=1, fill=1)

                pdf.setFont('Helvetica', 7)
                pdf.drawString(305,y-11,currencyInIndiaFormat('{0:.2f}'.format(basic_value))+' INR')
                if tax_type == 'SEZ':
                        pdf.drawString(390,y-11,'0.00 INR')
                        pdf.drawString(450,y-11,'0.00 INR')
                        pdf.drawString(510,y-11,currencyInIndiaFormat('{0:.2f}'.format(basic_value))+' INR')
                else:
                        gst = round(((total_value - basic_value) / 2),2)
                        pdf.drawString(390,y-11,currencyInIndiaFormat('{0:.2f}'.format(gst))+' INR')
                        pdf.drawString(450,y-11,currencyInIndiaFormat('{0:.2f}'.format(gst))+' INR')
                        pdf.drawString(510,y-11,currencyInIndiaFormat('{0:.2f}'.format(total_value))+' INR')

                y = y - 15
                pdf.rect(300,y,280,0.1, stroke=1, fill=1)
                y = y - 10
                return(y)
        
        else:
                pdf.rect(360,y,220,1, stroke=1, fill=1)
                pdf.setFillColor(HexColor('#E4E4E4'))
                pdf.rect(360,y-15,220,15, stroke=0, fill=1)
                #Colum headers
                pdf.setFillColor(HexColor('#000000'))
                pdf.setFont('Helvetica-Bold', 7)
                
                pdf.drawString(365,y-11,'Total Basic Value')
                pdf.drawString(450,y-11,'Total IGST')
                pdf.drawString(510,y-11,'Grand Total')
                y = y - 15
                pdf.rect(360,y,220,0.1, stroke=1, fill=1)

                pdf.setFont('Helvetica', 7)
                pdf.drawString(365,y-11,currencyInIndiaFormat('{0:.2f}'.format(basic_value))+' INR')
                if tax_type == 'SEZ':
                        pdf.drawString(450,y-11,'0.00 INR')
                        pdf.drawString(510,y-11,currencyInIndiaFormat('{0:.2f}'.format(basic_value))+' INR')
                else:
                        gst = round((total_value - basic_value),2)
                        pdf.drawString(450,y-11,currencyInIndiaFormat('{0:.2f}'.format(gst))+' INR')
                        pdf.drawString(510,y-11,currencyInIndiaFormat('{0:.2f}'.format(total_value))+' INR')

                y = y - 15
                pdf.rect(360,y,220,0.1, stroke=1, fill=1)
                y = y - 10
                return(y)

#add grand total
def add_amount_in_word(pdf,y,invoice_no,amount,tax_type):
        #Page Break
        if y < 50:
                y = add_new_page(pdf,invoice_no,tax_type)
                pdf.setFont('Helvetica', 9)

        pdf.rect(20,y,560,0.1, stroke=1, fill=1)
        wrapper = textwrap.TextWrapper(width=160) 
        word_list = wrapper.wrap(text=amount)
        y = y - 11
        pdf.setFillColor(HexColor('#000000'))
        pdf.setFont('Helvetica-Bold', 8)
        for element in word_list:
                pdf.drawString(20,y,element)
                y = y - 8
        pdf.rect(20,y,560,0.1, stroke=1, fill=1)
        y = y - 8
        return(y)

#add bank details
def add_bank_details(pdf,y,invoice_no,tax_type,bank_name,account_holder,account_no,ifcs_code,account_type):
        #Page Break
        if y < 80:
                y = add_new_page(pdf,invoice_no,tax_type)
        
        pdf.setFont('Helvetica-Bold', 7)
        pdf.drawString(20,y,'Bank Details')
        pdf.setFillColor(HexColor('#E4E4E4'))
        pdf.rect(20,y-43,250,40, stroke=0, fill=1)
        pdf.setFillColor(HexColor('#000000'))
        y = y - 10
        pdf.setFont('Helvetica', 7)
        pdf.drawString(20,y,'Name : ' + account_holder)

        pdf.setFont('Helvetica-Bold', 9)
        pdf.drawString(320,y,'For : Aeprocurex Sourcing Private Limited')
        pdf.setFont('Helvetica', 7)
        y = y - 10
        pdf.drawString(20,y, account_type + ' : ' + account_no)
        y = y - 10
        pdf.drawString(20,y, 'Bank : ' + bank_name)
        y = y - 10
        pdf.drawString(20,y, 'IFCS Code : ' + ifcs_code)
        pdf.drawString(515,y-10, 'Authorized Signature')
        y = y - 10

        return(y)

#Add terms & decl
def add_tc(pdf,y,invoice_no,tax_type):
        if y < 80:
                y = add_new_page(pdf,invoice_no,tax_type)
        pdf.setFont('Helvetica-Bold', 7)
        pdf.drawString(20,y,'Terms & Conditions')
        y = y - 9
        pdf.setFont('Helvetica', 7)
        pdf.drawString(20,y,'18% interest will be charged if the bill is not paid before due date.')
        y = y - 12
        pdf.setFont('Helvetica-Bold', 7)
        pdf.drawString(20,y,'Declaration')
        y = y - 9
        pdf.setFont('Helvetica', 7)
        pdf.drawString(20,y,'We decleare that this invoice shows the actual price of the goods described and that all particulars are true and correct.')
        y = y - 10

        return(y)

#def other info
def add_other_info(pdf,y,invoice_no,tax_type,remarks,info1,info2,info3,info4,info5,info6,info7):
        if y < 50:
                y = add_new_page(pdf,invoice_no,tax_type)
        if remarks != '' and remarks != 'None':
                pdf.setFont('Helvetica-Bold', 7)
                pdf.drawString(20,y,'Remarks : ' + remarks)
                y = y - 10
        if y < 50:
                y = add_new_page(pdf,invoice_no,tax_type)
        if info1 != '' and info1 != 'None':
                pdf.setFont('Helvetica-Bold', 7)
                pdf.drawString(20,y,info1)
                y = y - 10
        if y < 50:
                y = add_new_page(pdf,invoice_no,tax_type)
        if info2 != '' and info2 != 'None':
                pdf.setFont('Helvetica-Bold', 7)
                pdf.drawString(20,y,info2)
                y = y - 10
        if y < 50:
                y = add_new_page(pdf,invoice_no,tax_type)
        if info3 != '' and info3 != 'None':
                pdf.setFont('Helvetica-Bold', 7)
                pdf.drawString(20,y,info3)
                y = y - 10
        if y < 50:
                y = add_new_page(pdf,invoice_no,tax_type)
        if info4 != '' and info4 != 'None':
                pdf.setFont('Helvetica-Bold', 7)
                pdf.drawString(20,y,info4)
                y = y - 10
        if y < 50:
                y = add_new_page(pdf,invoice_no,tax_type)
        if info5 != '' and info5 != 'None':
                pdf.setFont('Helvetica-Bold', 7)
                pdf.drawString(20,y,info5)
                y = y - 10
        if y < 50:
                y = add_new_page(pdf,invoice_no,tax_type)
        if info6 != '' and info6 != 'None':
                pdf.setFont('Helvetica-Bold', 7)
                pdf.drawString(20,y,info6)
                y = y - 10
        if y < 50:
                y = add_new_page(pdf,invoice_no,tax_type)
        if info7 != '' and info7 != 'None':
                pdf.setFont('Helvetica-Bold', 7)
                pdf.drawString(20,y,info7)
                y = y - 10
        return(y)


##-------------------------------Invoice Acknowledgement-----------------------------------------------------
#Pending Acknowledgement list
@login_required(login_url="/employee/login/")
def invoice_pending_ack_list(request):
        context={}
        context['invoice_ack'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                pending_list = InvoiceTracker.objects.filter(generating_status='Generated',acknowledgement='No').values(
                        'invoice_no',
                        'invoice_date',
                        'customer__name',
                        'customer__location',
                        'po_reference',
                        'po_date',
                        'basic_value',
                        'total_value'
                )
                context['pending_list'] = pending_list

                if type == 'Accounts':
                        return render(request,"Accounts/InvoiceAck/pending_invoice_list.html",context)

#Pending Acknowledgement invoice details
@login_required(login_url="/employee/login/")
def invoice_pending_ack_details(request, invoice_no):
        context={}
        context['invoice_ack'] = 'active'
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

                ack_list = AcknowledgeDocument.objects.filter(invoice = invoice)

                context['invoice_lineitem'] = invoice_lineitems
                context['invoice'] = invoice
                context['invoice_no'] = invoice_no
                context['ack_list'] = ack_list

                if type == 'Accounts':
                        return render(request,"Accounts/InvoiceAck/invoice_selected_lineitem.html",context)

        if request.method == 'POST':
                data = request.POST
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)

                AcknowledgeDocument.objects.create(
                        invoice = invoice,
                        description = data['document_description'],
                        date = data['document_date'],
                        document = request.FILES['attachment']
                )
                return HttpResponseRedirect(reverse('invoice-pending-ack-list',args=[invoice_no]))

#Acknowledge invoice
@login_required(login_url="/employee/login/")
def invoice_acknowledge(request, invoice_no):
        context={}
        context['invoice_ack'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)
                doc_count = AcknowledgeDocument.objects.filter(invoice = invoice).count()

                if doc_count == 0:
                        return JsonResponse({'Message' : 'No Document Found'})
                
                invoice.acknowledgement = 'Yes'
                invoice.save()

                return JsonResponse({'Message' : 'Success'})

#Acknowledgeed Invoice list
@login_required(login_url="/employee/login/")
def invoice_ack_list(request):
        context={}
        context['invoice_ack'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                pending_list = InvoiceTracker.objects.filter(generating_status='Generated',acknowledgement='Yes').values(
                        'invoice_no',
                        'invoice_date',
                        'customer__name',
                        'customer__location',
                        'po_reference',
                        'po_date',
                        'basic_value',
                        'total_value'
                )
                context['pending_list'] = pending_list

                if type == 'Accounts':
                        return render(request,"Accounts/InvoiceAck/acknowledged_invoice_list.html",context)

#Acknowledged invoice details
@login_required(login_url="/employee/login/")
def invoice_ack_details(request, invoice_no):
        context={}
        context['invoice_ack'] = 'active'
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

                ack_list = AcknowledgeDocument.objects.filter(invoice = invoice)

                context['invoice_lineitem'] = invoice_lineitems
                context['invoice'] = invoice
                context['invoice_no'] = invoice_no
                context['ack_list'] = ack_list

                if type == 'Accounts':
                        return render(request,"Accounts/InvoiceAck/ack_invoice_lineitem.html",context)


#Acknowledged invoice edit
@login_required(login_url="/employee/login/")
def invoice_ack_edit(request, invoice_no):
        context={}
        context['invoice_ack'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                invoice = InvoiceTracker.objects.get(invoice_no = invoice_no)               
                invoice.acknowledgement = 'No'
                invoice.save()

                return JsonResponse({'Message' : 'Success'})
