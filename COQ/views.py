from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from State.models import StateList
from RFP.models import *
from Sourcing.models import *
import random


@login_required(login_url="/employee/login/")
def coq_pending_list(request):
    context={}
    context['COQ'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == "GET":
            rfp = RFP.objects.filter(opportunity_status='Open',enquiry_status='Sourcing_Completed').values(
                            'rfp_no',
                            'product_heading',
                            'rfp_type',
                            'customer__name',
                            'customer__location',
                            'customer_contact_person__name',
                            'rfp_creation_details__creation_date',
                            'rfp_sourcing_detail__sourcing_completed_by__first_name',
                            'priority'
                            )    
            context['rfp_list'] = rfp
        return render(request,"Sales/COQ/pending_list.html",context)

@login_required(login_url="/employee/login/")
def coq_pending_details(request,rfp_no=None):
    context={}
    context['COQ'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method == "GET":
            rfp_lineitems = RFPLineitem.objects.filter(rfp_no=rfp_no).values(
                'lineitem_id',
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
                'quantity',
                'target_price',
                'remarks',
                'customer_lead_time'
            )
            context['lineitems'] = rfp_lineitems

            sourcing_lineitems = SourcingLineitem.objects.filter(sourcing__rfp__rfp_no=rfp_no).values(
                'id',
                'rfp_lineitem__lineitem_id',
                'sourcing__supplier__name',
                'sourcing__supplier__location',
                'product_title',
                'description',
                'model',
                'brand',
                'product_code',
                'pack_size',
                'moq',
                'lead_time',
                'price_validity',
                'expected_freight',
                'mrp',
                'price1',
                'price2',
                'mark'
            ).order_by('price2')
            context['sourcing_lineitems'] = sourcing_lineitems

            sourcing_attachment = SourcingAttachment.objects.filter(sourcing__rfp__rfp_no = rfp_no)
            context['sourcing_attachment'] = sourcing_attachment

            other_cost = SourcingCharges.objects.filter(sourcing__rfp__rfp_no = rfp_no)
            context['other_cost'] = other_cost

            return render(request,"Sales/COQ/pending_details.html",context)

        if request.method == "POST":
            cl = COQLineitem.objects.filter(rfp_no = rfp_no)
            for c in cl:
                c.delete()

            sourcing_lineitem_object = SourcingLineitem.objects.filter(sourcing__rfp__rfp_no=rfp_no,mark='True')
            if sourcing_lineitem_object.count() == 0:
                context['error'] = 'Please select atleast one product'
                return render(request,"Sales/COQ/error.html",context)


            rfp_object = RFP.objects.get(rfp_no=rfp_no)
            print(rfp_object.rfp_type)

            if rfp_object.rfp_type == 'PSP':
                total_buying_value = 0
                for item in sourcing_lineitem_object:
                    total_buying_value = total_buying_value + (item.price1 * item.rfp_lineitem.quantity)

                if total_buying_value <= 250000:
                    for lineitem in sourcing_lineitem_object:
                        print(lineitem.id)
                        COQLineitem.objects.create(
                            id=lineitem.id+str(random.randint(100000,9999999)),
                            sourcing_lineitem=lineitem,
                            rfp_no = rfp_no,
                            product_title = lineitem.product_title,
                            description = lineitem.description,
                            model = lineitem.model,
                            brand = lineitem.brand,
                            product_code = lineitem.product_code,
                            pack_size = lineitem.pack_size,
                            moq = lineitem.moq,
                            hsn_code = lineitem.rfp_lineitem.hsn_code,
                            gst = lineitem.rfp_lineitem.gst,
                            quantity = lineitem.rfp_lineitem.quantity,
                            uom = lineitem.rfp_lineitem.uom,
                            expected_freight = lineitem.expected_freight,
                            unit_price = lineitem.price1,
                            lead_time = lineitem.lead_time,
                            margin = 2.0,
                            creation_time = lineitem.creation_time
                            )
                else:
                    for lineitem in sourcing_lineitem_object:
                        print(lineitem.id)
                        COQLineitem.objects.create(
                            id=lineitem.id+str(random.randint(100000,9999999)),
                            sourcing_lineitem=lineitem,
                            rfp_no = rfp_no,
                            product_title = lineitem.product_title,
                            description = lineitem.description,
                            model = lineitem.model,
                            brand = lineitem.brand,
                            product_code = lineitem.product_code,
                            pack_size = lineitem.pack_size,
                            moq = lineitem.moq,
                            hsn_code = lineitem.rfp_lineitem.hsn_code,
                            gst = lineitem.rfp_lineitem.gst,
                            quantity = lineitem.rfp_lineitem.quantity,
                            uom = lineitem.rfp_lineitem.uom,
                            expected_freight = lineitem.expected_freight,
                            unit_price = lineitem.price1,
                            lead_time = lineitem.lead_time,
                            margin = 1.0,
                            creation_time = lineitem.creation_time
                            )

            else:
                for lineitem in sourcing_lineitem_object:
                    print(lineitem.id)
                    COQLineitem.objects.create(
                        id=lineitem.id+str(random.randint(100000,9999999)),
                        sourcing_lineitem=lineitem,
                        rfp_no = rfp_no,
                        product_title = lineitem.product_title,
                        description = lineitem.description,
                        model = lineitem.model,
                        brand = lineitem.brand,
                        product_code = lineitem.product_code,
                        pack_size = lineitem.pack_size,
                        moq = lineitem.moq,
                        hsn_code = lineitem.rfp_lineitem.hsn_code,
                        gst = lineitem.rfp_lineitem.gst,
                        quantity = lineitem.rfp_lineitem.quantity,
                        uom = lineitem.rfp_lineitem.uom,
                        expected_freight = lineitem.expected_freight,
                        unit_price = lineitem.price2,
                        lead_time = lineitem.lead_time,
                        creation_time = lineitem.creation_time
                        )
            rfp_obj = RFP.objects.get(rfp_no=rfp_no)
            rfp_obj.enquiry_status = 'COQ Done'
            rfp_obj.save()

            sourcing_charges = SourcingCharges.objects.filter(sourcing__rfp__rfp_no = rfp_no)

            oc = OtherCharges.objects.filter(rfp = rfp_object)
            for item in oc:
                item.delete()
                
            for item in sourcing_charges:
                OtherCharges.objects.create(
                    rfp = rfp_object,
                    cost_description = item.cost_description,
                    value = item.value
                )

            return HttpResponseRedirect(reverse('coq_pending_list'))

@login_required(login_url="/employee/login/")
def coq_price_select(request,rfp_no=None,sourcing_id=None):
    context={}
    context['COQ'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method=="POST":
            sourcing_object = SourcingLineitem.objects.get(id=sourcing_id)
            if sourcing_object.mark == 'True':
                sourcing_object.mark = 'False'
            else:
                sourcing_object.mark = 'True'
            sourcing_object.save()
            return HttpResponseRedirect(reverse('coq_pending_details', args=[rfp_no]))

@login_required(login_url="/employee/login/")
def auto_coq(request,rfp_no=None):
    context={}
    context['COQ'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method=="POST":
            rfplineitems = RFPLineitem.objects.filter(rfp_no=rfp_no)
            
            for item in rfplineitems:
                try:
                    sourcing_items = SourcingLineitem.objects.filter(rfp_lineitem__lineitem_id=item.lineitem_id).order_by('price2')[0]
                    sourcing_items.mark = 'True'
                    sourcing_items.save()
                except:
                    pass
            return HttpResponseRedirect(reverse('coq_pending_details', args=[rfp_no]))

@login_required(login_url="/employee/login/")
def reset_coq(request,rfp_no=None):
    context={}
    context['COQ'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if type == 'Sales':
        if request.method=="POST":
            sourcing_lineitems = SourcingLineitem.objects.filter(sourcing__rfp__rfp_no=rfp_no)
            
            for item in sourcing_lineitems:
                item.mark='False'
                item.save()
            return HttpResponseRedirect(reverse('coq_pending_details', args=[rfp_no]))

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
            return HttpResponseRedirect(reverse('coq_pending_list'))

            