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
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                vpo_list = VendorPOTracker.objects.filter(order_status='Intransit')
                context['vpo_list'] = vpo_list

                if type == 'GRN':
                        return render(request,"GRN/GRN/VendorPO/intransit_list.html",context)

#Direct Processing Po Lineitem
@login_required(login_url="/employee/login/")
def IntransitSupplierPOLineitem(request,vpo_no=None):
        context={}
        context['invoice'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                vpo = VendorPOTracker.objects.get(po_number=vpo_no)
                vpo_lineitem = VendorPOLineitems.objects.filter(vpo=vpo.vpo)
                context['vpo_lineitem'] = vpo_lineitem

                if type == 'GRN':
                        return render(request,"GRN/GRN/VendorPO/intransit_lineitem.html",context)