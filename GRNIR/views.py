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

                #Check Creation  In Progress
                grnt_count = GRNTracker.objects.filter(vpo = vpo, status = 'creation_in_progress').count()

                if grnt_count > 0:
                        grnt = GRNTracker.objects.filter(vpo = vpo, status = 'creation_in_progress')[0]
                        return HttpResponseRedirect(reverse('grn-selected-lineitem',args=[grnt.grn_no]))

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
                        cpo = vpo.vpo.cpo,
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
                                        cpo_lineitem = vpo_lineitem.cpo_lineitem,
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

                context['vendor'] = grn.vendor.name
                context['location'] = grn.vendor.location

                if type == 'GRN':
                        return render(request,"GRN/GRN/VendorPO/grn_selected_lineitem.html",context)

#GRN Selected Lineitem Edit
@login_required(login_url="/employee/login/")
def GRNSelectedLineitemChangeQuantity(request,grn_no=None,item=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                grn_lineitem = GRNLineitem.objects.get(id=item)
                context['grn_lineitem'] = grn_lineitem

                if type == 'GRN':
                        return render(request,"GRN/GRN/VendorPO/grn_chnage_quantity.html",context)

        if request.method == 'POST':
                data = request.POST
                grn_lineitem = GRNLineitem.objects.get(id=item)

                try:
                        if float(data['quantity']) > grn_lineitem.vpo_lineitem.receivable_quantity:
                                return JsonResponse({'Message': 'Quantity Should be less or equalto then receivable quantity'})

                except:
                        if float(data['quantity']) > grn_lineitem.cpo_lineitem.direct_receivable_quantity:
                                return JsonResponse({'Message': 'Quantity Should be less or equalto then receivable quantity'})

                grn_lineitem.quantity = data['quantity']
                grn_lineitem.save()

                return HttpResponseRedirect(reverse('grn-selected-lineitem',args=[grn_no]))

#GRN Selected Lineitem Remove
@login_required(login_url="/employee/login/")
def GRNSelectedLineitemRemove(request,grn_no=None,item=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                grn_lineitem = GRNLineitem.objects.get(id=item)
                context['grn_lineitem'] = grn_lineitem

                if type == 'GRN':
                        return render(request,"GRN/GRN/VendorPO/remove_item.html",context)

        if request.method == 'POST':
                data = request.POST
                grn_lineitem = GRNLineitem.objects.get(id=item)
                grn_lineitem.delete()

                return HttpResponseRedirect(reverse('grn-selected-lineitem',args=[grn_no]))


#GRN Delete
@login_required(login_url="/employee/login/")
def GRNDelete(request,grn_no=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                grn = GRNTracker.objects.get(grn_no = grn_no)
                grn.status = 'deleted'
                grn.save()

                return HttpResponseRedirect(reverse('intransit-supplier-po-list'))

#GRN Process Further
@login_required(login_url="/employee/login/")
def GRNProcessFurther(request,grn_no=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                grn = GRNTracker.objects.get(grn_no = grn_no)
                lineitem_count = GRNLineitem.objects.filter(grn = grn).count()

                context['grn_no'] = grn_no

                grn_attachment = GRNAttachment.objects.filter(grn = grn)
                context['grn_attachment'] = grn_attachment
 
                if lineitem_count == 0:
                        return JsonResponse({"Message" : "No Lineitem Found"})

                return render(request,"GRN/GRN/VendorPO/grn_proceed.html",context)


#GRN Document
@login_required(login_url="/employee/login/")
def AddGRNDocument(request,grn_no=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                data = request.POST
                grn = GRNTracker.objects.get(grn_no = grn_no)
                
                GRNAttachment.objects.create(
                        grn = grn,
                        description = data['document_description'],
                        document_no = data['document_no'],
                        document_date = data['document_date'],
                        attachment = request.FILES['attachment']
                )

                return HttpResponseRedirect(reverse('grn-process-further',args=[grn_no]))

def vpo_status_changer(po_number):
        vpo = VendorPOTracker.objects.get(po_number = po_number)
        vpo_lineitem = VendorPOLineitems.objects.filter(vpo = vpo.vpo)

        for item in vpo_lineitem:
                if item.receivable_quantity > 0:
                        return

        vpo.status = 'GRN_Complete'
        vpo.save()
        return

def cpo_status_changer(id):
        cpo = CustomerPO.objects.get(id = id)
        cpo_lineitem = CPOLineitem.objects.filter(cpo = cpo)

        #cpo.status = 'Partial_Product_Received'
        #cpo.save()

        for item in cpo_lineitem:
                if item.direct_receivable_quantity > 0:
                        return

        cpo.status = 'Full_Product_Received'
        cpo.save()
        return


#Complete GRN
@login_required(login_url="/employee/login/")
def CompleteGRN(request,grn_no=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                grn = GRNTracker.objects.get(grn_no = grn_no)
                
                grn_lineitem = GRNLineitem.objects.filter(grn=grn)

                lineitem_count = GRNLineitem.objects.filter(grn = grn).count()
                if lineitem_count == 0:
                        return JsonResponse({"Message" : "No Lineitem Found"})

                try:
                        for item in grn_lineitem:
                                item.vpo_lineitem.receivable_quantity = item.vpo_lineitem.receivable_quantity - item.quantity
                                item.vpo_lineitem.save()
                except:
                        for item in grn_lineitem:
                                item.cpo_lineitem.direct_receivable_quantity = item.cpo_lineitem.direct_receivable_quantity - item.quantity
                                item.cpo_lineitem.save()

                grn.status = 'completed'
                grn.save()

                try:
                        vpo_status_changer(grn.vpo.po_number)
                except:
                        cpo_status_changer(grn.cpo.id)

                return JsonResponse({'Message': 'Success'})




###----------------------------------Direct Processing Customer PO--------------------------


#Direct Processing Customer PO List
@login_required(login_url="/employee/login/")
def DirectProcessingCustomerPOList(request):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo_list = CustomerPO.objects.filter(status='direct_processing').values(
                        'id',
                        'customer__name',
                        'customer__location',
                        'customer_po_no',
                        'customer_po_date',
                        'customer_contact_person__name',
                        'cpo_assign_detail__assign_to__first_name',
                        'cpo_assign_detail__assign_to__last_name'
                )
                context['cpo_list'] = cpo_list

                if type == 'GRN':
                        return render(request,"GRN/GRN/CustomerPO/direct_processing_list.html",context)


#Direct Processing Customer PO Lineitems
@login_required(login_url="/employee/login/")
def DirectProcessingCustomerPOLineitems(request, cpo_no=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo = CustomerPO.objects.get(id=cpo_no)
                cpo_lineitems = CPOLineitem.objects.filter(cpo = cpo)
                context['cpo_lineitems'] = cpo_lineitems
                context['cpo_no'] = cpo_no

                if type == 'GRN':
                        return render(request,"GRN/GRN/CustomerPO/direct_processing_lineitems.html",context)


#Direct Processing Customer PO Lineitems
@login_required(login_url="/employee/login/")
def DirectProcessingCustomerPOVendorSelection(request, cpo_no=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name


        cpo = CustomerPO.objects.get(id=cpo_no)

        #Check Creation  In Progress
        grnt_count = GRNTracker.objects.filter(cpo = cpo, status = 'creation_in_progress').count()

        if grnt_count > 0:
                grnt = GRNTracker.objects.filter(cpo = cpo, status = 'creation_in_progress')[0]
                return HttpResponseRedirect(reverse('grn-selected-lineitem',args=[grnt.grn_no]))

        if request.method == 'GET':
                vendor_list = SupplierProfile.objects.all()
                context['vendor_list'] = vendor_list
                context['cpo_no'] = cpo_no

                if type == 'GRN':
                        return render(request,"GRN/GRN/CustomerPO/vendor_selection.html",context)


#Direct Processing Product Selection
@login_required(login_url="/employee/login/")
def DirectProcessingCustomerPOProductSelection(request, cpo_no=None, vendor_id=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                cpo = CustomerPO.objects.get(id=cpo_no)
                cpo_lineitems = CPOLineitem.objects.filter(cpo = cpo, direct_receivable_quantity__gte = 1)
                context['cpo_lineitems'] = cpo_lineitems
                context['cpo_no'] = cpo_no

                if type == 'GRN':
                        return render(request,"GRN/GRN/CustomerPO/direct_processing_lineitem_selection.html",context)

        if request.method == 'POST':
                data = request.POST
                items = data['item_list']
                item_list = items.split(",")

                cpo = CustomerPO.objects.get(id = cpo_no)
                vendor = SupplierProfile.objects.get(id = vendor_id)

                financial_year = get_financial_year(datetime.datetime.today().strftime('%Y-%m-%d'))
                grn_count = (GRNTracker.objects.filter(financial_year = financial_year).count()) + 1
                grn_no = 'AG' +  financial_year + "{:04d}".format(grn_count)

                grn = GRNTracker.objects.create(
                        grn_no = grn_no,
                        cpo = cpo,
                        vendor = vendor,
                        grn_by = u,
                        financial_year = financial_year
                )


                for item in item_list:
                        if item != '':
                                cpo_lineitem = CPOLineitem.objects.get(id = item)
                                GRNLineitem.objects.create(
                                        grn = grn,
                                        cpo_lineitem = cpo_lineitem,
                                        product_title = cpo_lineitem.product_title,
                                        description = cpo_lineitem.description,
                                        model = cpo_lineitem.model,
                                        brand = cpo_lineitem.brand,
                                        product_code = cpo_lineitem.product_code,
                                        hsn_code = cpo_lineitem.hsn_code,
                                        pack_size = cpo_lineitem.pack_size,
                                        uom = cpo_lineitem.uom,
                                        quantity = cpo_lineitem.direct_receivable_quantity,
                                        unit_price = 0,
                                        gst = cpo_lineitem.gst

                                )
                
                return JsonResponse({"grn_no" : grn_no})