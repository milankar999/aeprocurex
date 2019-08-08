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
                vpo_list = VendorPOTracker.objects.filter(Q(order_status='Intransit', status='Approved') | Q(order_status='Partial Intransit', status='Approved')).values(
                        'po_number',
                        'vpo__vendor__name',
                        'vpo__vendor__location',
                        'po_date',
                        'vpo__requester__first_name',
                        'vpo__requester__last_name',
                        'order_status'
                )
                context['vpo_list'] = vpo_list

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/VendorPO/intransit_list.html",context)

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

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/VendorPO/intransit_lineitem.html",context)

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

                vpo_lineitem = VendorPOLineitems.objects.filter(vpo = vpo.vpo, receivable_quantity__gt = 0)
                context['vpo_lineitem'] = vpo_lineitem
                context['vpo_no'] = vpo_no

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/VendorPO/grn_lineitem_selection.html",context)

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
                                
                                item_total_price = round((float(vpo_lineitem.receivable_quantity) * float(vpo_lineitem.unit_price)),2)
                                item_total_price_with_gst = round((item_total_price + (item_total_price * float(vpo_lineitem.gst) / 100)),2)
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
                                        unit_price = vpo_lineitem.unit_price,
                                        gst = vpo_lineitem.gst,
                                        total_basic_price = item_total_price,
                                        total_price = item_total_price_with_gst
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

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/VendorPO/grn_selected_lineitem.html",context)

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

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/VendorPO/grn_chnage_quantity.html",context)

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

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/VendorPO/remove_item.html",context)

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

                return render(request,"Accounts/GRN/VendorPO/grn_proceed.html",context)


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
        vpo.order_status = 'Received'
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
                        try:
                                for item in grn_lineitem:
                                        item.cpo_lineitem.direct_receivable_quantity = item.cpo_lineitem.direct_receivable_quantity - item.quantity
                                        item.cpo_lineitem.save()
                        except:
                                pass


                grn.status = 'completed'
                grn.save()

                try:
                        vpo_status_changer(grn.vpo.po_number)
                except:
                        try:
                                cpo_status_changer(grn.cpo.id)
                        except:
                                pass

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

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/CustomerPO/direct_processing_list.html",context)


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

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/CustomerPO/direct_processing_lineitems.html",context)


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

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/CustomerPO/vendor_selection.html",context)


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

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/CustomerPO/direct_processing_lineitem_selection.html",context)

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
                        financial_year = financial_year,
                        grn_type = 'deirect_processing_customer_po'
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


##-----------------------------------------------------Direct GRN------------------------------------------------

#Direct GRN Vendor Selection
@login_required(login_url="/employee/login/")
def DirectGRNVendorSelection(request):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                vendor_list = SupplierProfile.objects.all()
                context['vendor_list'] = vendor_list

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/DirectGRN/vendor_selection.html",context)

        if request.method == 'POST':
                data = request.POST
                vendor_id = data['vendor_id']
                print(vendor_id)

                vendor = SupplierProfile.objects.get(id = vendor_id)

                financial_year = get_financial_year(datetime.datetime.today().strftime('%Y-%m-%d'))
                grn_count = (GRNTracker.objects.filter(financial_year = financial_year).count()) + 1
                grn_no = 'AG' +  financial_year + "{:04d}".format(grn_count)

                GRNTracker.objects.create(
                        grn_no = grn_no,
                        vendor = vendor,
                        grn_by = u,
                        financial_year = financial_year,
                        grn_type = 'direct_material_received'
                )
                return JsonResponse({'Message' : 'Success','grn_no' : grn_no})


#Deirect GRN Product Selection
@login_required(login_url="/employee/login/")
def DirectGRNProductEntry(request, grn_no=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                grn = GRNTracker.objects.get(grn_no = grn_no)
                grn_lineitem = GRNLineitem.objects.filter(grn = grn)

                context['grn_lineitem'] = grn_lineitem
                context['vendor_name'] = grn.vendor.name
                context['vendor_location'] = grn.vendor.location
                context['grn_no'] = grn_no

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/DirectGRN/grn_lineitem.html",context)

        if request.method == 'POST':
                data = request.POST

                grn = GRNTracker.objects.get(grn_no=grn_no)

                total_basic_price = 0
                try:
                        total_basic_price = round((float(data['unit_price']) * float(data['quantity'])),2)
                except:
                        pass
                
                total_price = 0
                try:
                        total_price = round((total_basic_price + round((total_basic_price * float(data['gst']) / 100),2)), 2)
                except:
                        pass


                g = GRNLineitem.objects.create(
                        grn = grn,
                        product_title = data['product_title'],
                        description = data['description'],
                        model = data['model'],
                        brand = data['brand'],
                        product_code = data['product_code'],
                        hsn_code = data['hsn_code'],
                        pack_size = data['pack_size'],
                        uom = data['uom'],
                        quantity = data['quantity'],
                        unit_price = data['unit_price'],
                        gst = data['gst'],
                        total_basic_price = total_basic_price,
                        total_price = total_price
                )

                print(g.grn.grn_no)
                return HttpResponseRedirect(reverse('direct-grn-product-entry',args=[grn_no]))


#Deirect GRN Product edit
@login_required(login_url="/employee/login/")
def DirectGRNProductEdit(request, grn_no=None, lineitem_id=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                grn_lineitem = GRNLineitem.objects.get(id=lineitem_id)

                context['grn_lineitem'] = grn_lineitem

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/DirectGRN/grn_lineitem_edit.html",context)

        if request.method == 'POST':
                data = request.POST
                grn_lineitem = GRNLineitem.objects.get(id=lineitem_id)

                print(grn_lineitem.product_title)
                grn_lineitem.product_title = data['product_title']
                grn_lineitem.description = data['description']
                grn_lineitem.model = data['model']
                grn_lineitem.brand = data['brand']
                grn_lineitem.product_code = data['product_code']
                grn_lineitem.pack_size = data['pack_size']
                grn_lineitem.uom = data['uom']
                grn_lineitem.quantity = data['quantity']
                grn_lineitem.unit_price = data['unit_price']
                grn_lineitem.gst = data['gst']

                total_basic_price = 0
                try:
                        total_basic_price = round((float(data['unit_price']) * float(data['quantity'])),2)
                except:
                        pass
                
                total_price = 0
                try:
                        total_price = round((total_basic_price + round((total_basic_price * float(data['gst']) / 100),2)), 2)
                except:
                        pass

                grn_lineitem.total_basic_price = total_basic_price
                grn_lineitem.total_price = total_price

                grn_lineitem.save()
                return HttpResponseRedirect(reverse('direct-grn-product-entry',args=[grn_no]))

#Deirect GRN Product delete
@login_required(login_url="/employee/login/")
def DirectGRNProductDelete(request, grn_no=None, lineitem_id=None):
        context={}
        context['grn'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                grn_lineitem = GRNLineitem.objects.get(id=lineitem_id)

                context['grn_lineitem'] = grn_lineitem

                if type == 'Accounts':
                        return render(request,"Accounts/GRN/DirectGRN/grn_lineitem_delete.html",context)

        if request.method == 'POST':
                grn_lineitem = GRNLineitem.objects.get(id=lineitem_id)
                grn_lineitem.delete()

                return HttpResponseRedirect(reverse('direct-grn-product-entry',args=[grn_no]))




##-----------------------------------------------------------------------Manage Inwards---------------------------------------------------------------------

#Inwards list by grn
@login_required(login_url="/employee/login/")
def InwardsByGRN(request):
        context={}
        context['inwards'] = 'active'
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
                    'ir_status',
                    'grn_type'
                )
                context['grn_list'] = grn_list

                if type == 'Accounts':
                        return render(request,"Accounts/Inwards/all_grn_list.html",context)

#Inwards list by items
@login_required(login_url="/employee/login/")
def InwardsByItems(request):
        context={}
        context['inwards'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
    
        if request.method == 'GET':
                grn_lineitem = GRNLineitem.objects.filter(grn__status = 'completed').values(
                    'grn__grn_no',
                    'grn__vpo__po_number',
                    'grn__vendor__name',
                    'product_title',
                    'description',
                    'model',
                    'brand',
                    'quantity',
                    'uom',
                    'grn__ir_status'
                )
                context['grn_lineitem'] = grn_lineitem
                

                if type == 'Accounts':
                        return render(request,"Accounts/Inwards/all_item_list.html",context)

#inward grn details
@login_required(login_url="/employee/login/")
def InwardGRNDetails(request, grn_no=None):
        context={}
        context['inwards'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                grn = GRNTracker.objects.get(grn_no = grn_no)
                grn_lineitem = GRNLineitem.objects.filter(grn = grn).values(
                        'id',
                        'product_title',
                        'description',
                        'model',
                        'brand',
                        'product_code',
                        'hsn_code',
                        'uom',
                        'quantity',
                        'unit_price',
                        'total_basic_price',
                        'gst',
                        'total_price'
                )

                context['grn_lineitem'] = grn_lineitem
                context['vendor_name'] = grn.vendor.name
                context['vendor_location'] = grn.vendor.location
                context['grn_no'] = grn_no
                context['grn_date'] = grn.date

                if type == 'Accounts':
                        return render(request,"Accounts/Inwards/grn_details.html",context)

#inward grn delete
@login_required(login_url="/employee/login/")
def InwardGRNDelete(request, grn_no=None):
        context={}
        context['inwards'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                grn = GRNTracker.objects.get(grn_no = grn_no)

                if grn.grn_type == 'regular':
                        grn_lineitem = GRNLineitem.objects.filter(grn = grn)
                        for item in grn_lineitem:
                                item.vpo_lineitem.receivable_quantity = item.vpo_lineitem.receivable_quantity + item.quantity
                                item.vpo_lineitem.save()

                        grn.status = 'deleted'
                        grn.save()
                        grn.vpo.status='Approved'
                        grn.vpo.order_status = 'Intransit'
                        grn.vpo.save()
                        return HttpResponseRedirect(reverse('intransit-supplier-po-list'))
                
                elif grn.grn_type == 'direct_material_received':
                        grn.status = 'deleted'
                        grn.save()
                        return HttpResponseRedirect(reverse('inwards-by-grn'))


##----------------------------------------------------------------------Invoice Receive---------------------------------------------------------------------------------------------

#Pending List
@login_required(login_url="/employee/login/")
def IRPendingList(request):
        context={}
        context['ir'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                grn_list = GRNTracker.objects.filter(Q(status = 'completed') & Q(ir_status = 'incomplete')).values(
                        'grn_no',
                        'vendor__name',
                        'vendor__location',
                        'date',
                        'vpo__po_number',
                        'vpo__po_date'
                )
                context['grn_list'] = grn_list

                if type == 'Accounts':
                        return render(request,"Accounts/IR/pending_list.html",context)

#Pending Lineitem
@login_required(login_url="/employee/login/")
def IRPendingGRNLineitem(request, grn_no=None):
        context={}
        context['ir'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                grn = GRNTracker.objects.get(grn_no = grn_no)
                grn_lineitem = GRNLineitem.objects.filter(grn = grn).values(
                        'id',
                        'product_title',
                        'description',
                        'model',
                        'brand',
                        'product_code',
                        'hsn_code',
                        'uom',
                        'quantity',
                        'unit_price',
                        'total_basic_price',
                        'gst',
                        'total_price'
                )

                total_basic_value = 0
                total_value = 0

                for item in grn_lineitem:
                        total_basic_value = total_basic_value + item['total_basic_price']
                        total_value = total_value + item['total_price']

                context['total_basic_value'] = total_basic_value
                context['total_value'] = total_value
                context['vendor_name'] = grn.vendor.name
                context['vendor_location'] = grn.vendor.location
                context['grn_no'] = grn_no
                context['grn_date'] = grn.date
                context['grn_lineitem'] = grn_lineitem
                try:
                        context['currency'] = grn.vpo.vpo.currency.currency_code
                except:
                        context['currency'] = 'INR'

                
                
                currency_list = CurrencyIndex.objects.all()
                context['currency_list'] = currency_list

                try:
                        context['current_currency'] = grn.vpo.vpo.currency
                        context['conversion_rate'] = grn.vpo.vpo.inr_value

                except:
                        context['current_currency'] = CurrencyIndex.DEFAULT_PK
                        context['conversion_rate'] = 1

                if type == 'Accounts':
                        return render(request,"Accounts/IR/pending_grn_lineitems.html",context)

        if request.method == 'POST':

                grn = GRNTracker.objects.get(grn_no = grn_no)
                grn_lineitem_count = GRNLineitem.objects.filter(grn=grn).count()

                if grn_lineitem_count < 1 :
                        return JsonResponse({'Message' : 'No Lineitem Found'})

                grn_lineitem = GRNLineitem.objects.filter(grn = grn)

                #for item in grn_lineitem:
                #        if item.unit_price < 0.01:
                #                return JsonResponse({'Message' : 'Lineitem Price Missing'})

                #        if item.gst < 0.01:
                #                return JsonResponse({'Message' : 'GST % Not Found'})

                total_basic_value = 0
                total_value = 0
                actual_total_basic_value = 0
                actual_total_value = 0

                for item in grn_lineitem:
                        total_basic_value = total_basic_value + item.total_basic_price
                        total_value = total_value + item.total_price

                total_basic_value = round(total_basic_value, 2)
                total_value = round(total_value , 2)

                data = request.POST
                
                actual_total_basic_value = round((total_basic_value * float(data['conversion_rate'])), 2)
                actual_total_value = round((total_value * float(data['conversion_rate'])), 2)

                currency = data['currency']
                cl = currency.split("/")
                currency_index = CurrencyIndex.objects.get(currency = cl[0].strip())

                ir_count = IRTracker.objects.filter(grn = grn).count()

                if ir_count > 0:
                        ir_list = IRTracker.objects.filter(grn = grn)
                        ir = ir_list[0]
                        
                        ir.invoice_no = data['invoice_no']
                        ir.invoice_date = data['invoice_date']
                        ir.total_basic_price = total_basic_value
                        ir.total_price = total_value
                        ir.received_currency = currency_index
                        ir.inr_value = data['conversion_rate']
                        ir.converted_total_basic_price = actual_total_basic_value
                        ir.converted_total_price = actual_total_value
                        ir.save()
                        ir_id = ir.id
                    
                else:
                        ir = IRTracker.objects.create(
                                grn = grn,
                                invoice_no = data['invoice_no'],
                                invoice_date = data['invoice_date'],
                                total_basic_price = total_basic_value,
                                total_price = total_value,
                                received_currency = currency_index,
                                inr_value = data['conversion_rate'],
                                converted_total_basic_price = actual_total_basic_value,
                                converted_total_price = actual_total_value
                        )
                        ir_id = ir.id
                return HttpResponseRedirect(reverse('invoice-received-add-invoice',args=[grn_no,ir_id]))

#Add extra items
@login_required(login_url="/employee/login/")
def IRPendingGRNAddExtraItem(request, grn_no=None):
        context={}
        context['ir'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                if type == 'Accounts':
                        grn = GRNTracker.objects.get(grn_no = grn_no)
                        data = request.POST

                        total_basic_price = float(data['quantity']) * float(data['unit_price'])
                        total_price = total_basic_price + (total_basic_price * float(data['gst']) / 100)

                        GRNLineitem.objects.create(
                                grn = grn,
                                product_title = data['product_title'],
                                description = data['description'],
                                model = data['model'],
                                brand = data['brand'],
                                product_code = data['product_code'],
                                hsn_code = data['hsn_code'],
                                pack_size = data['pack_size'],
                                uom = data['uom'],
                                quantity = data['quantity'],
                                unit_price = data['unit_price'],
                                gst = data['gst'],
                                total_basic_price = total_basic_price,
                                total_price = total_price
                        )

                        return HttpResponseRedirect(reverse('invoice-received-pending-grn-lineitem',args=[grn_no]))

#Lineitem Change Price
@login_required(login_url="/employee/login/")
def IRLineitemPriceChange(request, grn_no=None, lineitem_id = None):
        context={}
        context['ir'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                lineitem = GRNLineitem.objects.get(id = lineitem_id)
                context['grn_lineitem'] = lineitem

                if type == 'Accounts':
                        return render(request,"Accounts/IR/ir_change_price.html",context)

        if request.method == 'POST':
                lineitem = GRNLineitem.objects.get(id = lineitem_id)
                data = request.POST

                lineitem.hsn_code = data['hsn_code']
                lineitem.unit_price = data['unit_price']
                lineitem.gst = data['gst']

                total_basic_price = round((lineitem.quantity * float(lineitem.unit_price)),2) 
                lineitem.total_basic_price = total_basic_price

                total_price = round((total_basic_price + (total_basic_price * float(lineitem.gst) / 100)),2)
                lineitem.total_price = total_price
                lineitem.save()

                return HttpResponseRedirect(reverse('invoice-received-pending-grn-lineitem',args=[grn_no]))

#Add Supplier Invoice 
@login_required(login_url="/employee/login/")
def IRPendingGRNAddInvoice(request, grn_no=None, ir_id = None):
        context={}
        context['ir'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                ir = IRTracker.objects.get(id = ir_id)
                ir_attachment = IRAttachment.objects.filter(ir = ir)

                context['ir_attachment'] = ir_attachment
                context['grn_no'] = grn_no
                context['ir_id'] = ir_id
                if type == 'Accounts':
                        return render(request,"Accounts/IR/ir_add_document.html",context)

        if request.method == 'POST':
                data = request.POST
                ir = IRTracker.objects.get(id = ir_id)
                
                IRAttachment.objects.create(
                        ir = ir,
                        description = data['document_description'],
                        document_no = data['document_no'],
                        document_date = data['document_date'],
                        attachment = request.FILES['attachment']
                )
                return HttpResponseRedirect(reverse('invoice-received-add-invoice',args=[grn_no,ir_id]))

#Add Supplier Invoice 
@login_required(login_url="/employee/login/")
def IRComplete(request, grn_no=None, ir_id = None):
        context={}
        context['ir'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                grn = GRNTracker.objects.get(grn_no = grn_no)
                ir = IRTracker.objects.get(id = ir_id)

                ir_attachment_count = IRAttachment.objects.filter(ir = ir).count()
                if ir_attachment_count < 1:
                        return JsonResponse({'Message': 'Attachment Not Found'})

                grn.ir_status = 'completed'
                grn.save()

                return JsonResponse({'Message': 'Success'})

#Received Linvoice List
@login_required(login_url="/employee/login/")
def ReceivedInvoiceList(request):
        context={}
        context['ir'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                ir_list = IRTracker.objects.filter(grn__status = 'completed').values(
                        'id',
                        'invoice_no',
                        'invoice_date',
                        'total_basic_price',
                        'total_price',
                        'received_currency',
                        'grn__grn_no',
                        'grn__vendor__name',
                        'grn__vpo__po_number',
                        'grn__vpo__po_date'
                )
                context['ir_list'] = ir_list

                if type == 'Accounts':
                        return render(request,"Accounts/IR/received_invoice_list.html",context)

#Received Invoice Details
@login_required(login_url="/employee/login/")
def ReceivedInvoiceDetails(request, id=None):
        context={}
        context['ir'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                ir = IRTracker.objects.get(id=id)
                grn = ir.grn
                grn_lineitem = GRNLineitem.objects.filter(grn = grn).values(
                        'id',
                        'product_title',
                        'description',
                        'model',
                        'brand',
                        'product_code',
                        'hsn_code',
                        'uom',
                        'quantity',
                        'unit_price',
                        'total_basic_price',
                        'gst',
                        'total_price'
                )

                total_basic_value = 0
                total_value = 0

                for item in grn_lineitem:
                        total_basic_value = total_basic_value + item['total_basic_price']
                        total_value = total_value + item['total_price']

                context['total_basic_value'] = total_basic_value
                context['total_value'] = total_value
                context['vendor_name'] = grn.vendor.name
                context['vendor_location'] = grn.vendor.location
                context['grn_no'] = grn.grn_no
                context['grn_date'] = grn.date
                context['grn_lineitem'] = grn_lineitem
                try:
                        context['currency'] = grn.vpo.vpo.currency.currency_code
                except:
                        context['currency'] = 'INR'

                
                
                currency_list = CurrencyIndex.objects.all()
                context['currency_list'] = currency_list

                try:
                        context['current_currency'] = grn.vpo.vpo.currency
                        context['conversion_rate'] = grn.vpo.vpo.inr_value

                except:
                        context['current_currency'] = CurrencyIndex.DEFAULT_PK
                        context['conversion_rate'] = 1

                context['ir'] = ir

                irAttachment = IRAttachment.objects.filter(ir=ir).values(
                        'description',
                        'document_no',
                        'document_date',
                        'attachment'
                )
                context['irAttachment'] = irAttachment

                if type == 'Accounts':
                        return render(request,"Accounts/IR/received_invoice_details.html",context)

#Received Invoice Details Edit
@login_required(login_url="/employee/login/")
def ReceivedInvoiceDetailsEdit(request, id=None):
        context={}
        context['ir'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                ir = IRTracker.objects.get(id=id)
                grn = ir.grn
                grn_lineitem = GRNLineitem.objects.filter(grn = grn).values(
                        'id',
                        'product_title',
                        'description',
                        'model',
                        'brand',
                        'product_code',
                        'hsn_code',
                        'uom',
                        'quantity',
                        'unit_price',
                        'total_basic_price',
                        'gst',
                        'total_price'
                )

                total_basic_value = 0
                total_value = 0

                for item in grn_lineitem:
                        total_basic_value = total_basic_value + item['total_basic_price']
                        total_value = total_value + item['total_price']

                context['total_basic_value'] = total_basic_value
                context['total_value'] = total_value
                context['vendor_name'] = grn.vendor.name
                context['vendor_location'] = grn.vendor.location
                context['grn_no'] = grn.grn_no
                context['grn_date'] = grn.date
                context['grn_lineitem'] = grn_lineitem
                try:
                        context['currency'] = grn.vpo.vpo.currency.currency_code
                except:
                        context['currency'] = 'INR'

                
                
                currency_list = CurrencyIndex.objects.all()
                context['currency_list'] = currency_list

                try:
                        context['current_currency'] = grn.vpo.vpo.currency
                        context['conversion_rate'] = grn.vpo.vpo.inr_value

                except:
                        context['current_currency'] = CurrencyIndex.DEFAULT_PK
                        context['conversion_rate'] = 1

                if type == 'Accounts':
                        return render(request,"Accounts/IR/received_invoice_edit.html",context)

        if request.method == 'POST':

                ir = IRTracker.objects.get(id=id)
                grn = ir.grn
                grn_no = grn.grn_no
                grn_lineitem_count = GRNLineitem.objects.filter(grn=grn).count()

                if grn_lineitem_count < 1 :
                        return JsonResponse({'Message' : 'No Lineitem Found'})

                grn_lineitem = GRNLineitem.objects.filter(grn = grn)

                for item in grn_lineitem:
                        if item.unit_price < 0.01:
                                return JsonResponse({'Message' : 'Lineitem Price Missing'})

                        if item.gst < 0.01:
                                return JsonResponse({'Message' : 'GST % Not Found'})

                total_basic_value = 0
                total_value = 0
                actual_total_basic_value = 0
                actual_total_value = 0

                for item in grn_lineitem:
                        total_basic_value = total_basic_value + item.total_basic_price
                        total_value = total_value + item.total_price

                total_basic_value = round(total_basic_value, 2)
                total_value = round(total_value , 2)

                data = request.POST
                
                actual_total_basic_value = round((total_basic_value * float(data['conversion_rate'])), 2)
                actual_total_value = round((total_value * float(data['conversion_rate'])), 2)

                currency = data['currency']
                cl = currency.split("/")
                currency_index = CurrencyIndex.objects.get(currency = cl[0].strip())

                ir_count = IRTracker.objects.filter(grn = grn).count()

                if ir_count > 0:
                        ir_list = IRTracker.objects.filter(grn = grn)
                        ir = ir_list[0]
                        
                        ir.invoice_no = data['invoice_no']
                        ir.invoice_date = data['invoice_date']
                        ir.total_basic_price = total_basic_value
                        ir.total_price = total_value
                        ir.received_currency = currency_index
                        ir.inr_value = data['conversion_rate']
                        ir.converted_total_basic_price = actual_total_basic_value
                        ir.converted_total_price = actual_total_value
                        ir.save()
                        ir_id = ir.id
                    
                else:
                        ir = IRTracker.objects.create(
                                grn = grn,
                                invoice_no = data['invoice_no'],
                                invoice_date = data['invoice_date'],
                                total_basic_price = total_basic_value,
                                total_price = total_value,
                                received_currency = currency_index,
                                inr_value = data['conversion_rate'],
                                converted_total_basic_price = actual_total_basic_value,
                                converted_total_price = actual_total_value
                        )
                        ir_id = ir.id
                return HttpResponseRedirect(reverse('invoice-received-add-invoice',args=[grn_no,ir_id]))

