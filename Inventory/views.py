from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from GRNIR.models import *
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
def InventoryByGRN(request):
        context={}
        context['inventory'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                grn_list = GRNTracker.objects.filter(Q(status = 'completed') | Q(status = 'ir_completed')).values(
                    'grn_no',
                    'vpo__po_number',
                    'vpo__po_date',
                    'vendor__name',
                    'vendor__location',
                    'date',
                    'ir_status'
                )
                context['grn_list'] = grn_list

                if type == 'GRN':
                        return render(request,"GRN/Inventory/all_grn_list.html",context)