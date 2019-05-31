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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import Image, Paragraph, Table, TableStyle
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
import textwrap
import datetime
import os
from django.views.static import serve
from django.http import FileResponse


@login_required(login_url="/employee/login/")
def generate_quotation_list(request):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == "GET":
            rfp = RFP.objects.filter(opportunity_status='Open',enquiry_status='COQ Done').values(
                            'rfp_no',
                            'rfp_type',
                            'customer__name',
                            'customer__location',
                            'customer_contact_person__name',
                            'rfp_creation_details__creation_date',
                            'rfp_sourcing_detail__sourcing_completed_by__first_name',
                            'priority'
                            )    
            context['rfp_list'] = rfp
        return render(request,"Sales/Quotation/pending_list.html",context)

@login_required(login_url="/employee/login/")
def generate_quotation_lineitem(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == "GET":
            coq_lineitems = COQLineitem.objects.filter(rfp_no=rfp_no).annotate(
                basic_value=F('unit_price') + (F('unit_price') * F('margin') / 100),
                total_basic_value = F('unit_price') + (F('unit_price') * F('margin') / 100) * F('quantity'),
                total_with_gst = (F('unit_price') + (F('unit_price') * F('margin') / 100) * F('quantity')) + ((F('unit_price') + (F('unit_price') * F('margin') / 100) * F('quantity'))*F('gst')/100), 
                total_buying_price = F('unit_price') * F('quantity'),
                total_buying_price_with_gst = (F('unit_price') * F('quantity')) + ((F('unit_price') * F('quantity')) * F('gst') / 100)
                ).values(
                'id',
                'product_title',
                'description',
                'model',
                'brand',
                'product_code',
                'part_number',
                'pack_size',
                'moq',
                'hsn_code',
                'gst',
                'quantity',
                'uom',
                'lead_time',
                'expected_freight',
                'unit_price',
                'margin',
                'sourcing_lineitem__rfp_lineitem__customer_lead_time',
                'sourcing_lineitem__sourcing__supplier__name',
                'sourcing_lineitem__sourcing__supplier__location',
                'basic_value',
                'total_basic_value',
                'total_with_gst',
                'total_buying_price',
                'total_buying_price_with_gst'
            )
            print(coq_lineitems)
            context['coq_lineitems'] = coq_lineitems

            return render(request,"Sales/Quotation/lineitems.html",context)

        if request.method == "POST":
            rfp_obj = RFP.objects.get(rfp_no=rfp_no)
            rfp_obj.enquiry_status = 'COQ Done'
            rfp_obj.save()
            return HttpResponseRedirect(reverse('coq_pending_list'))

@login_required(login_url="/employee/login/")
def generate_quotation_resourcing(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == 'POST':
            rfp_object = RFP.objects.get(rfp_no=rfp_no)
            rfp_object.enquiry_status = 'Approved'
            rfp_object.save()
            return HttpResponseRedirect(reverse('generate-quotation-list'))

@login_required(login_url="/employee/login/")
def generate_quotation_recoq(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == 'POST':
            rfp_object = RFP.objects.get(rfp_no=rfp_no)
            rfp_object.enquiry_status = 'Sourcing_Completed'
            rfp_object.save()
            return HttpResponseRedirect(reverse('generate-quotation-list'))


@login_required(login_url="/employee/login/")
def generate_quotation_lineitem_edit(request,rfp_no=None,item_id=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == "GET":
            quotation_lineitem = COQLineitem.objects.get(id=item_id)
            context['quotation_lineitem'] = quotation_lineitem
            return render(request,"Sales/Quotation/lineitem_edit.html",context)

        if request.method == "POST":
            data = request.POST
            quotation_lineitem = COQLineitem.objects.get(id=item_id)
            quotation_lineitem.product_title = data['product_title']
            quotation_lineitem.description = data['description']
            quotation_lineitem.model = data['model']
            quotation_lineitem.brand = data['brand']
            quotation_lineitem.product_code = data['product_code']
            quotation_lineitem.part_number = data['part_number']
            quotation_lineitem.pack_size = data['pack_size']
            quotation_lineitem.moq = data['moq']
            quotation_lineitem.hsn_code = data['hsn_code']
            quotation_lineitem.gst = data['gst']
            quotation_lineitem.quantity = data['quantity']
            quotation_lineitem.uom = data['uom']
            quotation_lineitem.unit_price = data['unit_price']
            quotation_lineitem.margin = data['margin']
            quotation_lineitem.lead_time = data['lead_time']
            quotation_lineitem.save()
            return HttpResponseRedirect(reverse('generate-quotation-lineitem',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_quotation_lineitem_delete(request,rfp_no=None,item_id=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "GET":
            quotation_lineitem = COQLineitem.objects.get(id=item_id)
            context['quotation_lineitem'] = quotation_lineitem
            return render(request,"Sales/Quotation/lineitem_delete.html",context)

        if request.method == "POST":
            quotation_lineitem = COQLineitem.objects.get(id=item_id)
            quotation_lineitem.delete()
            return HttpResponseRedirect(reverse('generate-quotation-lineitem',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_quotation_price_fixing(request,rfp_no=None,item_id=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "GET":
            quotation_lineitem = COQLineitem.objects.get(id=item_id)
            context['quotation_lineitem'] = quotation_lineitem
            return render(request,"Sales/Quotation/price_fixing.html",context)

        if request.method == "POST":
            quotation_lineitem = COQLineitem.objects.get(id=item_id)
            data = request.POST
            basic_price = data['basic_price']
            buying_price = quotation_lineitem.unit_price
            margin = (float(basic_price) - float(buying_price)) * 100 / float(buying_price)
            quotation_lineitem.margin=margin
            quotation_lineitem.save()
            return HttpResponseRedirect(reverse('generate-quotation-lineitem',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_quotation_lineitem_add(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "GET":
            return render(request,"Sales/Quotation/lineitem_add.html",context)

        if request.method == "POST":
            data = request.POST
            COQLineitem.objects.create(
                id=rfp_no+str(random.randint(100000,9999999)),
                rfp_no = rfp_no,
                product_title = data['product_title'],
                description = data['description'],
                model = data['model'],
                brand = data['brand'],
                product_code = data['product_code'],
                pack_size = data['pack_size'],
                moq = data['moq'],
                hsn_code = data['hsn_code'],
                gst = data['gst'],
                quantity = data['quantity'],
                uom = data['uom'],
                unit_price = data['unit_price'],
                margin = data['margin'],
                lead_time = data['lead_time']
            )
            return HttpResponseRedirect(reverse('generate-quotation-lineitem',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_quotation_fill_margin(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "POST":
            data = request.POST
            coqLineitem = COQLineitem.objects.filter(rfp_no=rfp_no)
            
            for item in coqLineitem:
                item.margin = data['margin']
                item.save()
            return HttpResponseRedirect(reverse('generate-quotation-lineitem',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_quotation_fill_leadtime(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "POST":
            data = request.POST
            coqLineitem = COQLineitem.objects.filter(rfp_no=rfp_no)
            
            for item in coqLineitem:
                item.lead_time = data['lead_time']
                item.save()
            return HttpResponseRedirect(reverse('generate-quotation-lineitem',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_quotation_fill_brand(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "POST":
            data = request.POST
            coqLineitem = COQLineitem.objects.filter(rfp_no=rfp_no)
            
            for item in coqLineitem:
                item.brand = data['brand']
                item.save()
            return HttpResponseRedirect(reverse('generate-quotation-lineitem',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_quotation_fill_moq(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "POST":
            data = request.POST
            coqLineitem = COQLineitem.objects.filter(rfp_no=rfp_no)
            
            for item in coqLineitem:
                item.moq = data['moq']
                item.save()
            return HttpResponseRedirect(reverse('generate-quotation-lineitem',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_quotation_process(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "GET":
            
            #Number of line item check
            item_number = COQLineitem.objects.filter(rfp_no=rfp_no).count()
            if item_number == 0:
                context['error'] = 'No Item found'
                return render(request,"Sales/Quotation/error.html",context)

            #GST Checking
            coq_item = COQLineitem.objects.filter(rfp_no=rfp_no)
            for item in coq_item:
                if item.gst < 1:
                    context['error'] = 'Empty GST Found'
                    return render(request,"Sales/Quotation/error.html",context)
            
            #Pack Size Check
            pack_size_count = COQLineitem.objects.filter(rfp_no=rfp_no,pack_size='').count()
            if pack_size_count != 0:
                context['error'] = 'Empty Pack Size found'
                return render(request,"Sales/Quotation/error.html",context)

            #Data Extraction           
            rfp_info = RFP.objects.filter(rfp_no=rfp_no).values(
                'customer__id',
                'customer__name',
                'customer__code',
                'customer__location',
                'customer__address',
                'customer__billing_address',
                'customer__shipping_address',
                'customer__vendor_code',
                'customer__payment_term',
                'customer__gst_number',
                'customer__tax_type',
                'reference'
            )[0]
            context['rfp_info'] = rfp_info


            #processing count
            processing_count = QuotationTracker.objects.filter(rfp=RFP.objects.get(rfp_no=rfp_no),status='processing').count()
            if processing_count == 1:
                processing_obj = QuotationTracker.objects.filter(rfp=RFP.objects.get(rfp_no=rfp_no),status='processing')[0]
                context['quotation_info'] = processing_obj
                print(str(processing_obj.quotation_date))
                return render(request,"Sales/Quotation/process.html",context)


            #revised check
            revised_count = QuotationTracker.objects.filter(rfp=RFP.objects.get(rfp_no=rfp_no)).count()
            if revised_count > 0:
                quoted_objects = QuotationTracker.objects.filter(rfp=RFP.objects.get(rfp_no=rfp_no))
                context['quoted_list'] = quoted_objects
                return render(request,"Sales/Quotation/repeate.html",context)



            customer_code = rfp_info['customer__code']
            quotation_count = QuotationTracker.objects.filter(customer=RFP.objects.get(rfp_no=rfp_no).customer).values('rfp').distinct().count() + 1
            QuotationTracker.objects.create(
                quotation_no = 'AQ-' + customer_code + '-' + format(quotation_count,'03d'),
                rfp = RFP.objects.get(rfp_no=rfp_no),
                customer =   RFP.objects.get(rfp_no=rfp_no).customer,
                customer_contact_person = RFP.objects.get(rfp_no=rfp_no).customer_contact_person,
                enquiry_reference = RFP.objects.get(rfp_no=rfp_no).reference,
                created_by = request.user,
                tc1 = '1. Purchase Order: Should contain Product code, Size, Qty(delivery Schedule HSN No. GST No with Delivery address)',
                tc2 = '2. InCo / Delivery Terms : DAP at all your location',
                tc3 = '3. GST: As per above quoted',
                tc4 = '4. Payment Term: '+ str(rfp_info['customer__payment_term']) +' Days Credit from the date of Invoice',
                tc5 = '5. Delivery: As per above details from the date of Purchase Order receipt'
            )
            processing_obj = QuotationTracker.objects.filter(rfp=RFP.objects.get(rfp_no=rfp_no),status='processing')[0]
            context['quotation_info'] = processing_obj

            return render(request,"Sales/Quotation/process.html",context)


            #contact_person_info = CustomerContactPerson.objects.get(rfp_no=)
        if request.method == 'POST':
            data = request.POST
            quotation_obj = QuotationTracker.objects.filter(rfp=RFP.objects.get(rfp_no=rfp_no),status='processing')[0]
            quotation_obj.quotation_date = data['quotation_date']
            quotation_obj.enquiry_reference = data['enquiry_reference']
            quotation_obj.price_validity = data['price_validity']
            
            if data['comments'] != 'None':
                quotation_obj.comments = data['comments']
            else:
                quotation_obj.comments=''
            
            if data['tc1'] != 'None':
                quotation_obj.tc1 = data['tc1']
            else:
                quotation_obj.tc1 = ''

            if data['tc2'] != 'None':
                quotation_obj.tc2 = data['tc2']
            else:
                quotation_obj.tc2 = ''

            if data['tc3'] != 'None':
                quotation_obj.tc3 = data['tc3']
            else:
                quotation_obj.tc3 = ''

            if data['tc4'] != 'None':
                quotation_obj.tc4 = data['tc4']
            else:
                quotation_obj.tc4 = ''

            if data['tc5'] != 'None':
                quotation_obj.tc5 = data['tc5']
            else:
                quotation_obj.tc5 = ''

            if data['tc6'] != 'None':
                quotation_obj.tc6 = data['tc6']
            else:
                quotation_obj.tc16 = ''

            if data['tc7'] != 'None':
                quotation_obj.tc7 = data['tc7']
            else:
                quotation_obj.tc7 = ''

            if data['tc8'] != 'None':
                quotation_obj.tc8 = data['tc8']
            else:
                quotation_obj.tc8 = ''

            if data['tc9'] != 'None':
                quotation_obj.tc9 = data['tc9']
            else:
                quotation_obj.tc9 = ''

            if data['tc10'] != 'None':
                quotation_obj.tc10 = data['tc10']
            else:
                quotation_obj.tc10 = ''
            
            quotation_obj.save()

            quotation_lineitem = QuotationLineitem.objects.filter(quotation = quotation_obj)
            for item in quotation_lineitem:
                item.delete()
            
            coq_item = COQLineitem.objects.filter(rfp_no=rfp_no)

            
            all_total_basic_value = 0
            all_total_value = 0

            for item in coq_item:

                basic_price = round((item.unit_price + (item.unit_price * item.margin / 100)),2)
                total_basic_price = round((basic_price * item.quantity),2)
                total_price = round((total_basic_price + (total_basic_price * item.gst / 100)),2)

                QuotationLineitem.objects.create(
                    quotation = quotation_obj,
                    sourcing_lineitem = item.sourcing_lineitem,
                    product_title = item.product_title,
                    description = item.description,
                    model = item.model,
                    brand = item.brand,
                    product_code = item.product_code,
                    part_number = item.part_number,
                    pack_size = item.pack_size,
                    moq = item.moq,
                    hsn_code = item.hsn_code,
                    gst = item.gst,
                    quantity = item.quantity,
                    uom = item.uom,
                    unit_price = item.unit_price,
                    margin = item.margin,
                    lead_time = item.lead_time,
                    creation_time = item.creation_time,
                    basic_price = basic_price,
                    total_basic_price = total_basic_price,
                    total_price = total_price
                )
                all_total_basic_value = round((all_total_basic_value + total_basic_price),2)
                all_total_value = round((all_total_value + total_price),2)
            
            print(all_total_basic_value)
            print(all_total_value)

            quotation_obj.total_basic_price = all_total_basic_value
            quotation_obj.total_price = all_total_value

            quotation_obj.save()
            
            return HttpResponseRedirect(reverse('generate-quotation-column-selection',args=[rfp_no,quotation_obj.quotation_no]))

@login_required(login_url="/employee/login/")
def generate_revised_existing(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "POST":
            data = request.POST
            quotation_obj = QuotationTracker.objects.get(quotation_no=data['q_number'])
            quotation_obj.status = 'processing'
            quotation_obj.save()
            return HttpResponseRedirect(reverse('generate-quotation-process',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_revised_new(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "POST":
            data = request.POST
            quotation_number = data['new_q_number']
            quo_count = QuotationTracker.objects.filter(quotation_no=quotation_number).count()
            if quo_count != 0:
                context['error'] = 'Quotation with is number already exist. Please try again'
                return render(request,"Sales/Quotation/error.html",context)
            
            rfp_info = RFP.objects.filter(rfp_no=rfp_no).values(
                'customer__id',
                'customer__name',
                'customer__code',
                'customer__location',
                'customer__address',
                'customer__billing_address',
                'customer__shipping_address',
                'customer__vendor_code',
                'customer__payment_term',
                'customer__gst_number',
                'customer__tax_type',
                'reference'
            )[0]
            context['rfp_info'] = rfp_info

            QuotationTracker.objects.create(
                quotation_no = quotation_number,
                rfp = RFP.objects.get(rfp_no=rfp_no),
                customer =   RFP.objects.get(rfp_no=rfp_no).customer,
                customer_contact_person = RFP.objects.get(rfp_no=rfp_no).customer_contact_person,
                enquiry_reference = RFP.objects.get(rfp_no=rfp_no).reference,
                created_by = request.user,
                tc1 = '1. Purchase Order: Should contain Product code, Size, Qty(delivery Schedule HSN No. GST No with Delivery address)',
                tc2 = '2. InCo / Delivery Terms : DAP at all your location',
                tc3 = '3. GST: As per above quoted',
                tc4 = '4. Payment Term: '+ str(rfp_info['customer__payment_term']) +' Days Credit from the date of Invoice',
                tc5 = '5. Delivery: As per above details from the date of Purchase Order receipt'
            )
            return HttpResponseRedirect(reverse('generate-quotation-process',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_quotation_edit_customer(request,rfp_no=None,cust_id=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == "GET":
            customer = CustomerProfile.objects.get(id=cust_id)
            context['Customer'] = customer
            state = StateList.objects.all()
            context['StateList'] = state
            
            return render(request,"Sales/Quotation/customer_edit.html",context)

        if request.method=="POST":
            custData = CustomerProfile.objects.get(id=cust_id)
            data = request.POST
            custData.name = data['name']
            custData.location = data['location']
            custData.code = data['code']
            custData.address = data['address']
            custData.billing_address=data['billing_address']
            custData.shipping_address=data['shipping_address']
            custData.city = data['city']
            custData.state = data['state']
            custData.pin = data['pin']
            custData.country = data['country']
            custData.office_email1 = data['officeemail1']
            custData.office_email2 = data['officeemail2']
            custData.office_phone1 = data['officephone1']
            custData.office_phone2 = data['officephone2']
            custData.gst_number = data['GSTNo']
            custData.vendor_code = data['VendorCode']
            custData.payment_term = data['PaymentTerm']
            custData.inco_term = data['IncoTerm']
            custData.tax_type = data['tax_type']
            custData.save()
            return HttpResponseRedirect(reverse('generate-quotation-process',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def generate_quotation_column_selection(request,rfp_no=None,quotation_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['rfp_no'] = rfp_no
        
    if type == 'Sales':
        if request.method == 'GET':
            return render(request,"Sales/Quotation/column_selection.html",context)

        if request.method == 'POST':
            data = request.POST
            
            gst_price = ''
            image = ''
            total_basic = ''
            total_basic_with_gst = ''

            for item in data:
                if item == 'gst_price':
                    gst_price = 'Yes'
                if item == 'image':
                    image = 'Yes'
                if item == 'total_basic':
                    total_basic = 'Yes'
                if item == 'total_basic_with_gst':
                    total_basic_with_gst = 'Yes'

            Quotation_Generator(quotation_no,gst_price,image,total_basic,total_basic_with_gst)
            try:
                filepath = 'static/doc/quotation/' + quotation_no + '.pdf'
                quotation_obj = QuotationTracker.objects.get(quotation_no=quotation_no)
                quotation_obj.status = 'Generated'
                quotation_obj.save()
                rfp_object = RFP.objects.get(rfp_no=rfp_no)
                rfp_object.enquiry_status = 'Quoted'
                rfp_object.save()
                return HttpResponseRedirect(reverse('download-quotation', args=[rfp_no,quotation_no]))
                #return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
            except:
                pass
            


            #return FileResponse('static/doc/quotation/'+quotation_no+'.pdf', as_attachment=True, filename= quotation_no + '.pdf')

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

def Add_Header(pdf):
    pdf.drawInlineImage("static/image/aeprocurex.jpg",360,750,220,70)
    pdf.setFont('Helvetica-Bold', 13)
    pdf.drawString(10,763,"AEPROCUREX SOURCING PRIVATE LIMITED")

    pdf.setFont('Helvetica', 10)
    #pdf.setFillColor(HexColor('#000000'))
    pdf.drawString(10,748,"Regd. Office: Shankarappa Complex, No.4")
    pdf.drawString(10,735,"Hosapalya Main Road, Opp. To Om Shakti Temple")
    pdf.drawString(10,722,"HSR Layout Extension,Bangalore - 560068")

    pdf.drawString(10,709,"Telephone: 080-43743314, +91 9964892600")
    pdf.drawString(10,696,"E-mail: sales.p@aeprocurex.com")
    pdf.drawString(10,683,"GST No. 29AAQCA2809L1Z6")

    pdf.setFont('Helvetica-Bold', 20)
    pdf.drawString(300,700,"QUOTATION")
    #pdf.setFillColor(yellow)
    pdf.rect(300,696,275,1, stroke=1, fill=1)

def Add_Footer(pdf):
    pdf.setFont('Helvetica', 10)
    pdf.drawString(250,15,'www.aeprocurex.com')
    pdf.drawString(520,15,'Page-No : ' + str(pdf.getPageNumber()))

def quotation_information(pdf,quotation_no,quotation_date,vendor_code,enquiry_reference,price_validity):
    if vendor_code == None:
        vendor_code = ' '

    pdf.setFont('Helvetica', 9)
    pdf.drawString(300,680,"Quotation No :")
    pdf.drawString(300,667,"Date :")
    pdf.drawString(300,654,"Price Validity :")
    pdf.drawString(300,635,"Enquiry Reference :")
    pdf.drawString(300,622,"Supplier Code :")

    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(390,680,quotation_no)
    pdf.drawString(390,667,str(quotation_date.strftime('%d, %b %Y')))
    pdf.drawString(390,654,price_validity)
    pdf.drawString(390,635,enquiry_reference)
    pdf.drawString(390,622,vendor_code)

def Add_To(pdf,customer_name,address,gst,shipping_address,billing_address):
    pdf.setFont('Helvetica-Bold', 13)
    pdf.drawString(10,622,'QUOTATION TO')
    pdf.rect(10,618,100,0.5, stroke=1, fill=1)
    #pdf.setFont('Helvetica-Bold', 13)

    pdf.setFont('Helvetica-Bold', 11)
    pdf.drawString(10,605,customer_name)
    pdf.setFont('Helvetica', 11)
    
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
    #Billing Address
    if billing_address == 'Same':
        billing_address = address
    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(10,y,'BILL TO')
    y = y - 11
    wrapper = textwrap.TextWrapper(width=140)
    word_list = wrapper.wrap(text=billing_address)
    pdf.setFont('Helvetica', 9)
    for element in word_list:
        pdf.drawString(10,y,element)
        y = y - 11

    y = y - 3
    #Shipping Address
    if shipping_address == 'Same':
        shipping_address = address
    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(10,y,'SHIP TO')
    y = y - 11
    word_list = wrapper.wrap(text=shipping_address)
    pdf.setFont('Helvetica', 9)
    for element in word_list:
        pdf.drawString(10,y,element)
        y = y - 11
    return(y)
       
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
    pdf.drawString(330,y-11,'Basic Price / UOM')
    pdf.drawString(348,y-22,'(IN INR)')
    pdf.drawString(420,y-11,'Total Basic Price')
    pdf.drawString(438,y-22,'(IN INR)')
    pdf.drawString(520,y-17,'Lead Time')
    y = y - 31
    pdf.rect(10,y,570,0.1, stroke=1, fill=1)
    return(y)

def add_lineitem(pdf,sl_no,product_title,description,model,brand,part_number,product_code,pack_size,moq,hsn_code,gst,quantity,uom,unit_price,lead_time,state,tax_type,gst_price,quotation_no,y):
    pdf.setFont('Helvetica', 9)
    pdf.drawString(12,y-10,str(sl_no))
    pdf.drawString(230,y-10,'{0:.2f}'.format(quantity))
    pdf.drawString(283,y-10,uom.upper())

    pdf.drawString(330,y-10,currencyInIndiaFormat(str(unit_price)))
    
    total_basic_price = '{0:.2f}'.format(float(unit_price)*quantity)
    pdf.drawString(420,y-10,currencyInIndiaFormat(total_basic_price))
    pdf.drawString(520,y-10,lead_time)

    #Product title
    material_wrapper = textwrap.TextWrapper(width=45)
    title_word_list = material_wrapper.wrap(text=product_title)
    
    #Page Break
    if y < 50:
        y = add_new_page(pdf,quotation_no)
        y = Add_Table_Header(pdf,y)
        pdf.setFont('Helvetica', 9)

    for element in title_word_list:
        pdf.drawString(40,y-10,element)
        y = y - 11
        
        #Page Break
        if y < 50:
            y = add_new_page(pdf,quotation_no)
            y = Add_Table_Header(pdf,y)
            pdf.setFont('Helvetica', 9)
    
    y=y-3
    #Description
    description_word_list = material_wrapper.wrap(description)
    for element in description_word_list:
        pdf.drawString(40,y-10,element)
        y = y - 11
    
        #Page Break
        if y < 50:
            y = add_new_page(pdf,quotation_no)
            y = Add_Table_Header(pdf,y)
            pdf.setFont('Helvetica', 9)

    y=y-3
    #model
    if brand != '' and brand != 'None':
        try:
            brand_word_list = material_wrapper.wrap('Make :' + brand)
            for element in brand_word_list:
                
                pdf.drawString(40,y-10,element)
                y = y - 11
                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 9)
            y=y-3
        except:
            pass

    #Make
    if model != '' and model !='None':
        try:
            model_word_list = material_wrapper.wrap('Model :' + model)
            for element in model_word_list:
                
                pdf.drawString(40,y-10,element)
                y = y - 11
                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 9)

            y=y-3
        except:
            pass

    #Product code
    if product_code != '' and product_code != 'None':
        try:
            product_code_word_list = material_wrapper.wrap('Manufacturer Part No :' + product_code)
            for element in product_code_word_list:
                pdf.drawString(40,y-10,element)
                y = y - 11

                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 9)
            y = y - 3
        except:
            pass

    #Part Number Code
    if part_number != '' and part_number != 'None':
        try:
            part_number_word_list = material_wrapper.wrap('Your Part Number :' + part_number)
            for element in part_number_word_list:
                pdf.drawString(40,y-10,element)
                y = y - 11
                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 9)
            y = y - 3
        except:
            pass
    
    y = y - 4
    #Additional Informations
    additional_info = ''
    if pack_size != '' and pack_size != 'None':
        try:
            additional_info = additional_info +'Pack Size -' + pack_size
        except:
            pass
   
    if moq != '' and moq != 'None':
        try:
            additional_info = additional_info + ', MOQ -' + moq
        except:
            pass
    
    if hsn_code != '' and hsn_code != 'None':
        try:
            additional_info = additional_info + ', HSN Code - ' + hsn_code
        except:
            pass

    if additional_info != '':
        try:
            material_wrapper = textwrap.TextWrapper(width=100)
            additional_info_word_list = material_wrapper.wrap('Additional Information : ' + additional_info)
            for element in additional_info_word_list:
                pdf.drawString(40,y-10,element)
                y = y - 11
                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 9)
        except:
            pass

    #Tax Information
    if gst != '':
        pdf.setFont('Helvetica-Bold', 8)
        pdf.drawString(330,y-10,'Tax Information')
        pdf.setFont('Helvetica', 8)
        y = y-11
        #Page Break
        if y < 50:
            y = add_new_page(pdf,quotation_no)
            y = Add_Table_Header(pdf,y)
            pdf.setFont('Helvetica', 8)
        gst_value = 0

        if tax_type == 'SEZ':
            gst_value = 0
            if state == 'Karnataka':
                pdf.drawString(330,y-10,'CGST  :    ' + '{0:.2f}'.format(0) + ' %')
                if gst_price == 'Yes':
                    pdf.drawString(450,y-10, '{0:.2f}'.format(0) + ' INR')

                y = y - 11
                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 8)
                pdf.drawString(330,y-10,'SGST  :    ' + '{0:.2f}'.format(0) + ' %')
                if gst_price == 'Yes':
                    pdf.drawString(450,y-10, '{0:.2f}'.format(0) + ' INR')
                y = y - 11
                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 8)
            else:
                pdf.drawString(330,y-10,'IGST  :    ' + '{0:.2f}'.format(0) + ' %')
                if gst_price == 'Yes':
                    pdf.drawString(450,y-10, '{0:.2f}'.format(0) + ' INR')
                y = y - 11
                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 8)

        else:
            gst_value = (float(total_basic_price) * gst / 100)
            if state == 'Karnataka':
                pdf.drawString(330,y-10,'CGST  :    ' + '{0:.2f}'.format(gst/2) + ' %')
                if gst_price == 'Yes':
                    pdf.drawString(450,y-10, currencyInIndiaFormat('{0:.2f}'.format(gst_value/2)) + ' INR')
                y = y - 11
                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 8)
                pdf.drawString(330,y-10,'SGST  :    ' + '{0:.2f}'.format(gst/2) + ' %')
                if gst_price == 'Yes':
                    pdf.drawString(450,y-10, currencyInIndiaFormat('{0:.2f}'.format(gst_value/2)) + ' INR')
                y = y - 11
                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 8)
            else:
                pdf.drawString(330,y-10,'IGST  :    ' + '{0:.2f}'.format(gst) + ' %')
                if gst_price == 'Yes':
                    pdf.drawString(450,y-10, currencyInIndiaFormat('{0:.2f}'.format(gst_value)) + ' INR')
                y = y - 11
                #Page Break
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    y = Add_Table_Header(pdf,y)
                    pdf.setFont('Helvetica', 8)
    
    if gst_price == 'Yes':
        y = y - 10
        #Page Break
        if y < 50:
            y = add_new_page(pdf,quotation_no)
            y = Add_Table_Header(pdf,y)
        pdf.setFont('Helvetica', 9)
        total_amount = float(total_basic_price) + float(gst_value)
        pdf.drawString(330,y-10,'Amount with Tax')
        pdf.drawString(450,y-10,currencyInIndiaFormat('{0:.2f}'.format(total_amount)) + ' INR')
        y = y - 11
        #Page Break
        if y < 50:
            y = add_new_page(pdf,quotation_no)
            y = Add_Table_Header(pdf,y)
            pdf.setFont('Helvetica', 9)
    y=y-5
    
    pdf.rect(10,y,570,0.1, stroke=1, fill=1)
    #Page Break
    if y < 50:
        y = add_new_page(pdf,quotation_no)
        y = Add_Table_Header(pdf,y)
        pdf.setFont('Helvetica', 9)
    return y

def add_total_basic(pdf,amount,quotation_no,y):
    y = y - 12
    #Page Break
    if y < 50:
        y = add_new_page(pdf,quotation_no)
    pdf.setFont('Helvetica', 9)
    pdf.drawString(330,y,'Total Basic Amount')
    pdf.drawString(450,y,currencyInIndiaFormat('{0:.2f}'.format(amount)) + ' INR')
    y = y -15
    if y < 50:
        y = add_new_page(pdf,quotation_no)
    return(y)

def add_total_with_gst(pdf,basic_amount,gst_amount,quotation_no,y):
    pdf.setFont('Helvetica', 8)
    pdf.drawString(330,y-12,'Total Basic Amount')
    pdf.drawString(450,y-12,currencyInIndiaFormat('{0:.2f}'.format(basic_amount)) + ' INR')
    y = y - 15
    if y < 50:
        y = add_new_page(pdf,quotation_no)
        pdf.setFont('Helvetica', 8)
    pdf.drawString(330,y-12,'Total Tax')
    pdf.drawString(450,y-12,currencyInIndiaFormat('{0:.2f}'.format(gst_amount)) + ' INR')
    y = y - 17
    if y < 50:
        y = add_new_page(pdf,quotation_no)
        pdf.setFont('Helvetica', 8)
    pdf.rect(330,y,250,0.1, stroke=1, fill=1)
    pdf.setFont('Helvetica-Bold', 8)
    pdf.drawString(330,y-12,'All Total')
    pdf.drawString(450,y-12,currencyInIndiaFormat('{0:.2f}'.format(basic_amount + gst_amount)) + ' INR')
    y =y -15
    if y < 50:
        y = add_new_page(pdf,quotation_no)
    return(y)

def add_tc(pdf,tc1,tc2,tc3,tc4,tc5,tc6,tc7,tc8,tc9,tc10,quotation_no,y):
    if y < 50:
        y = add_new_page(pdf,quotation_no)
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(10,y,'Commercial Terms and Conditions :')
    pdf.rect(10,y-3,150,0.1, stroke=1, fill=1)
    y = y - 14
    if y < 50:
        y = add_new_page(pdf,quotation_no)
    pdf.setFont('Helvetica', 8)
    wrapper = textwrap.TextWrapper(width=150) 
    
    #tc1
    if tc1 != '':
        try:
            word_list = wrapper.wrap(text=tc1)
            for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 10
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    pdf.setFont('Helvetica', 8)
            y = y -3
        except:
            pass

    #tc2
    if tc2 != '':
        try:
            word_list = wrapper.wrap(text=tc2)
            for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 10
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    pdf.setFont('Helvetica', 8)
            y = y -3
        except:
            pass

    #tc3
    if tc3 != '':
        try:
            word_list = wrapper.wrap(text=tc3)
            for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 10
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    pdf.setFont('Helvetica', 8)
            y = y -3
        except:
            pass

    #tc4
    if tc4 != '':
        try:
            word_list = wrapper.wrap(text=tc4)
            for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 10
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    pdf.setFont('Helvetica', 8)
            y = y -3
        except:
            pass

    #tc5
    if tc5 != '':
        try:
            word_list = wrapper.wrap(text=tc5)
            for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 10
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    pdf.setFont('Helvetica', 8)
            y = y -3
        except:
            pass

    #tc6
    if tc6 != '':
        try:
            word_list = wrapper.wrap(text=tc6)
            for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 10
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    pdf.setFont('Helvetica', 8)
            y = y -3
        except:
            pass           

    #tc7
    if tc7 != '':
        try:
            word_list = wrapper.wrap(text=tc7)
            for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 10
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    pdf.setFont('Helvetica', 8)
            y = y -3
        except:
            pass

    #tc8
    if tc8 != '':
        try:
            word_list = wrapper.wrap(text=tc8)
            for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 10
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    pdf.setFont('Helvetica', 8)
            y = y -3
        except:
            pass

    #tc9
    if tc9 != '':
        try:
            word_list = wrapper.wrap(text=tc9)
            for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 10
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    pdf.setFont('Helvetica', 8)
            y = y -3
        except:
            pass

    #tc10
    if tc10 != '':
        try:
            word_list = wrapper.wrap(text=tc10)
            for element in word_list:
                pdf.drawString(10,y,element)
                y = y - 10
                if y < 50:
                    y = add_new_page(pdf,quotation_no)
                    pdf.setFont('Helvetica', 8)
            y = y -3
        except:
            pass

def add_new_page(pdf,quotation_no):
    pdf.showPage()
    pdf.drawInlineImage("static/image/aeprocurex.jpg",360,750,220,70)
    Add_Footer(pdf)
    pdf.setFont('Helvetica-Bold', 13)
    pdf.drawString(10,763,'QUOTATION NO : ' + quotation_no)
    pdf.line(10,748,580,748)
    return(730)

def Quotation_Generator(quotation_no,gst_price,image,total_basic,total_basic_with_gst):

    #Extract Quotation Data
    quotation_obj = QuotationTracker.objects.get(quotation_no=quotation_no)
    quotation_lineitem = QuotationLineitem.objects.filter(quotation=quotation_obj).order_by('creation_time')
    pdf = canvas.Canvas("media/quotation/" + quotation_no + ".pdf", pagesize=A4)
    pdf.setTitle(quotation_no + '.pdf')
    Add_Header(pdf)
    Add_Footer(pdf)
    quotation_information(
        pdf,
        quotation_obj.quotation_no,
        quotation_obj.quotation_date,
        quotation_obj.customer.vendor_code,
        quotation_obj.enquiry_reference,
        quotation_obj.price_validity
    )      
    y = Add_To(
        pdf,
        quotation_obj.customer.name,
        quotation_obj.customer.address,
        quotation_obj.customer.gst_number,
        quotation_obj.customer.shipping_address,
        quotation_obj.customer.billing_address
        )
    y = Add_Table_Header(pdf,y)
    i = 1
    state = quotation_obj.customer.state
    tax_type = quotation_obj.customer.tax_type
    total_basic_amount = 0
    total_gst = 0
    for lineitem in quotation_lineitem:
        product_title = lineitem.product_title
        description = lineitem.description
        model = lineitem.model
        brand = lineitem.brand
        part_number = lineitem.part_number
        product_code = lineitem.product_code

        pack_size = lineitem.pack_size
        moq = lineitem.moq

        hsn_code = lineitem.hsn_code
        gst = lineitem.gst

        quantity = lineitem.quantity
        uom = lineitem.uom

        unit_price = '{0:.2f}'.format(lineitem.unit_price + (lineitem.unit_price * lineitem.margin /100))
        total_basic_amount = total_basic_amount + float('{0:.2f}'.format(float(unit_price) * float(quantity)))
        total_gst = total_gst + float('{0:.2f}'.format(float('{0:.2f}'.format(float(unit_price) * float(quantity))) * gst / 100))
        lead_time = lineitem.lead_time
        y = add_lineitem(pdf,i,product_title,description,model,brand,part_number,product_code,pack_size,moq,hsn_code,gst,quantity,uom,unit_price,lead_time,state,tax_type,gst_price,quotation_obj.quotation_no,y)
        i = i + 1

    if total_basic == 'Yes' and total_basic_with_gst != 'Yes':
        y = add_total_basic(pdf,total_basic_amount,quotation_obj.quotation_no,y)

    if total_basic_with_gst == 'Yes':
        y = add_total_with_gst(pdf,total_basic_amount,total_gst,quotation_obj.quotation_no,y)

    y = y -15
    #Comments
    #y = add_new_page(pdf,quotation_obj.quotation_no)
    if quotation_obj.comments != '':
        pdf.setFont('Helvetica-Bold', 9)
        wrapper = textwrap.TextWrapper(width=135) 
        word_list = wrapper.wrap(text='Note : ' + quotation_obj.comments)
        for element in word_list:
            pdf.drawString(10,y,element)
            y = y - 12
            if y < 30:
                y = add_new_page(pdf,quotation_obj.quotation_no)
        y = y - 15

    y = y - 12
    #Commercial terms & Conditions
    add_tc(pdf,quotation_obj.tc1,quotation_obj.tc2,quotation_obj.tc3,quotation_obj.tc4,quotation_obj.tc5,quotation_obj.tc6,quotation_obj.tc7,quotation_obj.tc8,quotation_obj.tc9,quotation_obj.tc10,quotation_obj.quotation_no,y)
        
    pdf.showPage()
    pdf.save()

@login_required(login_url="/employee/login/")
def download_quotation(request,rfp_no=None,quotation_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == "GET":
            context['quotation_no'] = quotation_no
            return render(request,"Sales/Quotation/download_quotation.html",context)

@login_required(login_url="/employee/login/")
def quoted_list(request):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == "GET":
            quoted_list = QuotationTracker.objects.filter(rfp__opportunity_status='Open',status='Generated').values(
                            'quotation_no',
                            'rfp__rfp_no',
                            'rfp__rfp_type',
                            'customer__name',
                            'customer__location',
                            'customer_contact_person__name',
                            'rfp__rfp_creation_details__creation_date',
                            'rfp__rfp_sourcing_detail__sourcing_completed_by__first_name',
                            'quotation_date',
                            'total_basic_price',
                            'total_price'
                            )    
            context['quoted_list'] = quoted_list
        return render(request,"Sales/Quotation/quoted_list.html",context)   

@login_required(login_url="/employee/login/")
def quoted_quotation_list(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == "GET":
            quoted_quotation_list = QuotationTracker.objects.filter(rfp__rfp_no=rfp_no).values(
                            'quotation_no',
                            'rfp__rfp_no',
                            'customer__name',
                            'customer__location',
                            'customer_contact_person__name',
                            'rfp__rfp_creation_details__creation_date',
                            'rfp__rfp_sourcing_detail__sourcing_completed_by__first_name',
                            'quotation_date',
                            'total_basic_price',
                            'total_price'
                            )    
            context['quoted_list'] = quoted_quotation_list
        return render(request,"Sales/Quotation/quoted_quotation_list.html",context)

@login_required(login_url="/employee/login/")
def quotation_lineitems(request,rfp_no=None,quotation_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == "GET":
            quotation_obj = QuotationTracker.objects.get(quotation_no=quotation_no)
            quotation_lineitem = QuotationLineitem.objects.filter(quotation = quotation_obj)
            context['quotation_lineitem'] = quotation_lineitem
            context['quotation_no'] = quotation_no
            return render(request,"Sales/Quotation/quoted_lineitems.html",context)

@login_required(login_url="/employee/login/")
def copy_quotation(request,rfp_no=None,quotation_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == 'GET':
            return render(request,"Sales/Quotation/column_selection.html",context)

        if request.method == 'POST':
            data = request.POST
            
            gst_price = ''
            image = ''
            total_basic = ''
            total_basic_with_gst = ''

            for item in data:
                if item == 'gst_price':
                    gst_price = 'Yes'
                if item == 'image':
                    image = 'Yes'
                if item == 'total_basic':
                    total_basic = 'Yes'
                if item == 'total_basic_with_gst':
                    total_basic_with_gst = 'Yes'

            Quotation_Generator(quotation_no,gst_price,image,total_basic,total_basic_with_gst)
            #return FileResponse('static/doc/quotation/'+quotation_no+'.pdf', as_attachment=True, filename= quotation_no + '.pdf')
            Quotation_Generator(quotation_no,gst_price,image,total_basic,total_basic_with_gst)
            return HttpResponseRedirect(reverse('download-quotation', args=[rfp_no,quotation_no]))

@login_required(login_url="/employee/login/")
def resourcing(request,rfp_no=None,quotation_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == 'POST':
            rfp_object = RFP.objects.get(rfp_no=rfp_no)
            rfp_object.enquiry_status = 'Approved'
            rfp_object.save()
            return HttpResponseRedirect(reverse('quotation_lineitems', args=[rfp_no,quotation_no]))

@login_required(login_url="/employee/login/")
def re_coq(request,rfp_no=None,quotation_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == 'POST':
            rfp_object = RFP.objects.get(rfp_no=rfp_no)
            rfp_object.enquiry_status = 'Sourcing_Completed'
            rfp_object.save()
            return HttpResponseRedirect(reverse('quotation_lineitems', args=[rfp_no,quotation_no]))

@login_required(login_url="/employee/login/")
def revised_quotation(request,rfp_no=None,quotation_no=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == 'POST':
            rfp_object = RFP.objects.get(rfp_no=rfp_no)
            rfp_object.enquiry_status = 'COQ Done'
            rfp_object.save()
            return HttpResponseRedirect(reverse('quotation_lineitems', args=[rfp_no,quotation_no]))

@login_required(login_url="/employee/login/")
def immediate_quotation_selection(request):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == 'GET':
            return render(request,"Sales/Quotation/Immediate_Quotation/quotation_type_selection.html",context)

@login_required(login_url="/employee/login/")
def immediate_quotation_customer_selection(request,quotation_type=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == 'GET':
            customer = CustomerProfile.objects.all()
            context['CustomerList'] = customer
            state = StateList.objects.all()
            context['StateList'] = state
            context['quotation_type'] = quotation_type
            return render(request,"Sales/Quotation/Immediate_Quotation/customer_selection.html",context)

        if request.method == "POST":
            user = User.objects.get(username=request.user)
            data = request.POST
            customer_id = 'C1' + str(format(CustomerProfile.objects.count() + 1, '04d'))
            cust = CustomerProfile.objects.create(id=customer_id,name=data['name'],location=data['location'],code=data['code'],address=data['address'],city=data['city'],state=data['state'],pin=data['pin'],country=data['country'],office_email1=data['officeemail1'],office_email2=data['officeemail2'],office_phone1=data['officephone1'],office_phone2=data['officephone2'],gst_number=data['GSTNo'],vendor_code=data['VendorCode'],payment_term=data['PaymentTerm'],inco_term=data['IncoTerm'],created_by=user)
            if cust:
                u = User.objects.get(username=request.user)
                type = u.profile.type
                customer = CustomerProfile.objects.all()
                context['CustomerList'] = customer
                state = StateList.objects.all()
                context['StateList'] = state
                context['message'] = 'Successfully registered ' + data['name']
                context['message_type'] = 'success'
                if type == 'Sales':
                    context['quotation_type'] = quotation_type
                    return render(request,"Sales/Quotation/Immediate_Quotation/customer_selection.html",context)
        
            else:
                u = User.objects.get(username=request.user)
                type = u.profile.type
                customer = CustomerProfile.objects.all()
                context['CustomerList'] = customer
                state = StateList.objects.all()
                context['StateList'] = state
                context['message'] = 'Something went wrong'
                context['message_type'] = 'danger'
                if type == 'Sales':
                    context['quotation_type'] = quotation_type
                    return render(request,"Sales/Quotation/Immediate_Quotation/customer_selection.html",context)

@login_required(login_url="/employee/login/")
def immediate_quotation_cperson_selection(request,quotation_type=None,cust_id=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == 'GET':
            ContactPerson = CustomerContactPerson.objects.filter(customer_name__pk=cust_id)
            context['ContactPerson'] = ContactPerson
            customer = CustomerProfile.objects.get(id=cust_id)
            context['CustomerName'] = customer.name
            context['CustomerID'] = cust_id
            context['quotation_type'] = quotation_type
            return render(request,"Sales/Quotation/Immediate_Quotation/contact_person_selection.html",context)

        if request.method == "POST":
            user = User.objects.get(username=request.user)
            data = request.POST
            customer = CustomerProfile.objects.get(id=cust_id)
            contactperson_id =  cust_id +'P' + str(CustomerContactPerson.objects.count() + 1)
            cp = CustomerContactPerson.objects.create(id=contactperson_id,name=data['name'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],customer_name=customer,created_by=user)
            if cp:
                context['message'] = 'Successfully registered ' + data['name']
                context['message_type'] = 'success'
            else:
                context['message'] = 'Something went wrong'
                context['message_type'] = 'danger'
      
            ContactPerson = CustomerContactPerson.objects.filter(customer_name__pk=cust_id)
            context['ContactPerson'] = ContactPerson
            customer = CustomerProfile.objects.get(id=cust_id)
            context['CustomerName'] = customer.name
            context['CustomerID'] = cust_id
            context['quotation_type'] = quotation_type
            return render(request,"Sales/Quotation/Immediate_Quotation/contact_person_selection.html",context)

@login_required(login_url="/employee/login/")
def immediate_quotation_enduser_selection(request,quotation_type=None,cust_id=None,contact_person_id=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['cust_id'] = cust_id
    context['contact_person_id'] = contact_person_id
    context['quotation_type'] = quotation_type
        
    if type == 'Sales':
        if request.method == 'GET':
            enduser = EndUser.objects.filter(customer_name__pk=cust_id)
            context['EndUser'] = enduser
            customer = CustomerProfile.objects.get(id=cust_id)
            context['CustomerName'] = customer.name
            return render(request,"Sales/Quotation/Immediate_Quotation/enduser_selection.html",context)

        if request.method == "POST":
            user = User.objects.get(username=request.user)
            data = request.POST
            customer = CustomerProfile.objects.get(id=cust_id)
            enduser_id =  cust_id +'D' + str(EndUser.objects.count() + 1)
            cp = EndUser.objects.create(id=enduser_id,user_name=data['name'],department_name = data['dept'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],customer_name=customer,created_by=user)
            if cp:
                context['message'] = 'Successfully registered ' + data['name']
                context['message_type'] = 'success'
            else:
                context['message'] = 'Something went wrong'
                context['message_type'] = 'danger'
            
            enduser = EndUser.objects.filter(customer_name__pk=cust_id)
            context['EndUser'] = enduser
            customer = CustomerProfile.objects.get(id=cust_id)
            context['CustomerName'] = customer.name
            return render(request,"Sales/Quotation/Immediate_Quotation/enduser_selection.html",context)

@login_required(login_url="/employee/login/")
def immediate_quotation_process(request,quotation_type=None,cust_id=None,contact_person_id=None,enduser_id=None):
    context={}
    context['quotation'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    context['cust_id'] = cust_id
    context['contact_person_id'] = contact_person_id
    context['quotation_type'] = quotation_type

    if request.method == "GET":
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        enduser = EndUser.objects.filter(customer_name__pk=cust_id)
        context['EndUser'] = enduser
        customer = CustomerProfile.objects.get(id=cust_id)
        rfp_no = 'RFP' + customer.id + customer.code + str(RFP.objects.count()+1) + '-INDP'
        customer = CustomerProfile.objects.get(id=cust_id)
        customer_contact_person = CustomerContactPerson.objects.get(id=contact_person_id)
        
        if enduser_id == 'none':
                creation_details = RFPCreationDetail.objects.create(id=rfp_no+'C1',created_by=user)
                new_rfp = RFP.objects.create(rfp_no=rfp_no,customer=customer,customer_contact_person=customer_contact_person,rfp_creation_details=creation_details,creation_type='INDEP')
        else:
                end_user = EndUser.objects.get(id=enduser_id)
                creation_details = RFPCreationDetail.objects.create(id=rfp_no+'C1',created_by=user)
                new_rfp = RFP.objects.create(rfp_no=rfp_no,customer=customer,customer_contact_person=customer_contact_person,end_user=end_user,rfp_creation_details=creation_details,creation_type='INDEP')
        context['rfp_no'] = rfp_no

        if new_rfp:
                if creation_details:
                        if type == 'Sales':
                                return render(request,"Sales/Quotation/Immediate_Quotation/process.html",context)
    
@login_required(login_url="/employee/login/")
def immediate_quotation_product_selection(request,rfp_no=None):
    context={}
    context['quotation'] = 'active'

    if request.method == "GET":
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        type = u.profile.type
        context['rfp_no'] = rfp_no

        lineitems = RFPLineitem.objects.filter(rfp_no__pk=rfp_no)
        context['lineitems'] = lineitems

        if type == 'Sales':
            return render(request,"Sales/Quotation/Immediate_Quotation/product_selection.html",context)

