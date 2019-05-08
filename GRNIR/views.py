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
from POForVendor.models import *
import random
from django.db.models import F
import textwrap
import datetime
import os
from django.views.static import serve
from django.http import FileResponse
from django.db.models import Q


#Direct processing PO
@login_required(login_url="/employee/login/")
def IntransitSupplierPOList(request):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                vpo_list = VendorPOTracker.objects.filter(order_status='Intransit', status='Approved').values(
                        'po_number',
                        'vpo__vendor__name',
                        'vpo__vendor__location',
                        'po_date',
                        'vpo__requester__first_name',
                        'vpo__requester__last_name'
                )
                context['vpo_list'] = vpo_list

                if type == 'GRN':
                        return render(request,"GRN/GRN/VendorPO/intransit_list.html",context)

#Direct Processing Po Lineitem
@login_required(login_url="/employee/login/")
def IntransitSupplierPOLineitem(request,vpo_no=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                vpo = VendorPOTracker.objects.get(po_number=vpo_no)
                vpo_lineitem = VendorPOLineitems.objects.filter(vpo=vpo.vpo)
                context['vpo_lineitem'] = vpo_lineitem
                context['vpo_no'] = vpo_no

                if type == 'GRN':
                        return render(request,"GRN/GRN/VendorPO/intransit_lineitem.html",context)

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


#Select GRN Lineitem
@login_required(login_url="/employee/login/")
def SelectGRNLineitem(request,vpo_no=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                vpo = VendorPOTracker.objects.get(po_number=vpo_no)
                vpo_lineitem = VendorPOLineitems.objects.filter(vpo = vpo.vpo, receivable_quantity__gte = 0)
                context['vpo_lineitem'] = vpo_lineitem
                context['vpo_no'] = vpo_no

                if type == 'GRN':
                        return render(request,"GRN/GRN/VendorPO/grn_lineitem_selection.html",context)

        if request.method == 'POST':
                data = request.POST
                items = data['item_list']
                item_list = items.split(",")
                
                vpo = VendorPOTracker.objects.get(po_number=vpo_no)
                
                financial_year = get_financial_year(datetime.datetime.today().strftime('%Y-%m-%d'))
                grn_count = (GRNTracker.objects.filter(financial_year = financial_year).count()) + 1
                grn_no = 'AG' +  financial_year + "{:04d}".format(grn_count)

                grn = GRNTracker.objects.create(
                        grn_no = grn_no,
                        vpo = vpo,
                        vendor = vpo.vpo.vendor,
                        grn_by = u,
                        financial_year = financial_year
                )

                for item in item_list:
                        if item != '':
                                vpo_lineitem = VendorPOLineitems.objects.get(id = item)
                                print(vpo_lineitem.product_title)
                                GRNLineitem.objects.create(
                                        grn = grn,
                                        vpo_lineitem = vpo_lineitem,
                                        product_title = vpo_lineitem.product_title,
                                        description = vpo_lineitem.description,
                                        model = vpo_lineitem.model,
                                        brand = vpo_lineitem.brand,
                                        product_code = vpo_lineitem.product_code,
                                        hsn_code = vpo_lineitem.hsn_code,
                                        pack_size = vpo_lineitem.pack_size,
                                        uom = vpo_lineitem.uom,
                                        quantity = vpo_lineitem.receivable_quantity,
                                        unit_price = 0,
                                        gst = vpo_lineitem.gst

                                )
                
                return JsonResponse({"grn_no" : grn_no})

#GRN Selected Lineitem
@login_required(login_url="/employee/login/")
def GRNSelectedLineitem(request,grn_no=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                grn = GRNTracker.objects.get(grn_no = grn_no)
                grn_lineitem = GRNLineitem.objects.filter(grn=grn)

                context['grn_no'] = grn_no
                context['grn_lineitem'] = grn_lineitem

                if type == 'GRN':
                        return render(request,"GRN/GRN/VendorPO/grn_selected_lineitem.html",context)

#GRN Selected Lineitem Edit
@login_required(login_url="/employee/login/")
def GRNSelectedLineitemEdit(request,grn_no=None,item=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                grn_lineitem = GRNLineitem.objects.get(id=item)
                context['grn_lineitem'] = grn_lineitem

                if type == 'GRN':
                        return render(request,"GRN/GRN/VendorPO/grn_lineitem_edit.html",context)
