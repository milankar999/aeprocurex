from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from POForVendor.models import *

@login_required(login_url="/employee/login/")
def VPOSelection(request):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                vpo = VendorPOTracker.objects.filter(payment_status = 'Pending', requester=u).values(
                    'po_number',
                    'po_date',
                    'basic_value',
                    'total_value',
                    'pending_payment_amount',
                    'vpo__vendor__name',
                    'vpo__vendor__location'
                )
                context['vpo_list'] = vpo

                if type == 'Sourcing':
                        return render(request,"Sourcing/SupplierPayment/vpo_selection.html",context)


@login_required(login_url="/employee/login/")
def NewPaymentRequest(request,po_number=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                vpo = VendorPOTracker.objects.get(po_number = po_number)
                spr_count = SupplierPaymentRequest.objects.filter(vpo = vpo, status = 'Requested').count()
                if spr_count > 0:
                        return JsonResponse({'Message': 'Payment Request already exist for this order'})

                context['pending_payment_amount'] = vpo.pending_payment_amount
                context['po_number'] = po_number
                return render(request,"Sourcing/SupplierPayment/new_payment_request.html",context)

        if request.method == 'POST':
                vpo = VendorPOTracker.objects.get(po_number=po_number)
                data = request.POST
                if float(data['amount']) > vpo.pending_payment_amount :
                        return JsonResponse({'Message': 'Amount Should not be greater than pending amount'})
                try:
                        myfile = request.FILES['supporting_document']
                        SupplierPaymentRequest.objects.create(
                            vpo = vpo,
                            amount = float(data['amount']),
                            notes = data['note'],
                            requester = u,
                            attachment1 = myfile
                        )
                except:
                        SupplierPaymentRequest.objects.create(
                            vpo = vpo,
                            amount = float(data['amount']),
                            notes = data['note'],
                            requester = u
                        )
                return HttpResponseRedirect(reverse('supplier-payment-applied-list'))

@login_required(login_url="/employee/login/")
def SupplierPaymentAppliedList(request):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name               

        if request.method == 'GET':
                request_list = SupplierPaymentRequest.objects.filter(
                        status = 'Requested',
                        requester = u
                ).values(
                        'id',   
                        'vpo__po_number',
                        'vpo__po_date',
                        'vpo__vpo__vendor__name',
                        'vpo__vpo__vendor__location',
                        'amount'
                )

                context['request_list'] = request_list
                return render(request,"Sourcing/SupplierPayment/applied_list.html",context)

@login_required(login_url="/employee/login/")
def SupplierPaymentRequestDelete(request, request_id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name     

        if request.method == 'GET':
                payment_request = SupplierPaymentRequest.objects.get(id = request_id)
                context['payment_request'] = payment_request

                if type == 'Sourcing':
                        return render(request,"Sourcing/SupplierPayment/delete_request.html",context)

        if request.method == 'POST':
                payment_request = SupplierPaymentRequest.objects.get(id = request_id)
                payment_request.delete()
                return HttpResponseRedirect(reverse('supplier-payment-applied-list'))


@login_required(login_url="/employee/login/")
def SupplierPaymentRequestEdit(request, request_id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name 

        if request.method == 'GET':
                payment_request = SupplierPaymentRequest.objects.get(id = request_id)
                context['payment_request'] = payment_request

                if type == 'Sourcing':
                        return render(request,"Sourcing/SupplierPayment/edit_request.html",context)

        if request.method == 'POST':
                data = request.POST
                payment_request = SupplierPaymentRequest.objects.get(id = request_id)
                payment_request.amount = data['amount']
                payment_request.notes = data['note']
                payment_request.save()

                try:
                        myfile = request.FILES['supporting_document']
                        payment_request.attachment1 = myfile
                        payment_request.save()
                
                except:
                        pass

                return HttpResponseRedirect(reverse('supplier-payment-applied-list'))

#Lavel1 Approval List 
@login_required(login_url="/employee/login/")
def SupplierPaymentPendingApprovalList1(request):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name 

        if u.profile.supplier_payment_user_type != 'L1':
                return JsonResponse({'Message': 'You are not allow to view this page'})

        if request.method == 'GET':
                request_list = SupplierPaymentRequest.objects.filter(
                        status = 'Requested'
                ).values(
                        'id',   
                        'vpo__po_number',
                        'vpo__po_date',
                        'vpo__vpo__vendor__name',
                        'vpo__vpo__vendor__location',
                        'vpo__vpo__terms_of_payment',
                        'vpo__vpo__requester__first_name',
                        'vpo__vpo__requester__last_name',
                        'amount'
                )

                context['request_list'] = request_list
                return render(request,"Sales/SupplierPayment/pending_approval_list_l1.html",context)

#Lavel1 Approval List 
@login_required(login_url="/employee/login/")
def SupplierPaymentPendingApprovalDetails1(request, request_id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name 

        if u.profile.supplier_payment_user_type != 'L1':
                return JsonResponse({'Message': 'You are not allow to view this page'})

        if request.method == 'GET':
                request_details = SupplierPaymentRequest.objects.get(id=request_id)
                context['request_details'] = request_details

                vpo_lineitem = VendorPOLineitems.objects.filter(vpo=request_details.vpo.vpo)
                context['vpo'] = request_details.vpo
                context['vpo_lineitem'] = vpo_lineitem

                if type == 'Sales':
                        return render(request,"Sales/SupplierPayment/pending_approval_details_l1.html",context)

#Lavel1 Reject 
@login_required(login_url="/employee/login/")
def SupplierPaymentPendingApprovalReject1(request, request_id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name 

        if u.profile.supplier_payment_user_type != 'L1':
                return JsonResponse({'Message': 'You are not allow to view this page'})

        if request.method == 'POST':
                request_details = SupplierPaymentRequest.objects.get(id=request_id)
                request_details.status = 'Rejected1'
                request_details.save()


                return HttpResponseRedirect(reverse('supplier-payment-pending-approval-list-1'))

#Lavel1 Approve 
@login_required(login_url="/employee/login/")
def SupplierPaymentPendingApprovalApprove1(request, request_id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name 

        if u.profile.supplier_payment_user_type != 'L1':
                return JsonResponse({'Message': 'You are not allow to view this page'})

        if request.method == 'POST':
                request_details = SupplierPaymentRequest.objects.get(id=request_id)
                request_details.status = 'Approved1'
                request_details.save()


                return HttpResponseRedirect(reverse('supplier-payment-pending-approval-list-1'))

#Label 1 Approved list for buyer
@login_required(login_url="/employee/login/")
def SupplierPaymentLabel1ApprovedList(request):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name               

        if request.method == 'GET':
                request_list = SupplierPaymentRequest.objects.filter(
                        status = 'Approved1',
                        requester = u
                ).values(
                        'id',   
                        'vpo__po_number',
                        'vpo__po_date',
                        'vpo__vpo__vendor__name',
                        'vpo__vpo__vendor__location',
                        'amount'
                )

                context['request_list'] = request_list
                return render(request,"Sourcing/SupplierPayment/label1_approve_list.html",context)

#Label 1 Rejected list for buyer
@login_required(login_url="/employee/login/")
def SupplierPaymentLabel1RejectList(request):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name               

        if request.method == 'GET':
                request_list = SupplierPaymentRequest.objects.filter(
                        status = 'Rejected1',
                        requester = u
                ).values(
                        'id',   
                        'vpo__po_number',
                        'vpo__po_date',
                        'vpo__vpo__vendor__name',
                        'vpo__vpo__vendor__location',
                        'amount'
                )

                context['request_list'] = request_list
                return render(request,"Sourcing/SupplierPayment/label1_reject_list.html",context)

#Supplier payment view request details
@login_required(login_url="/employee/login/")
def SupplierPaymentViewRequestDetails(request,request_id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name               

        if request.method == 'GET':
                payment_request = SupplierPaymentRequest.objects.get(id = request_id)
                context['payment_request'] = payment_request

                if type == 'Sourcing':
                        return render(request,"Sourcing/SupplierPayment/view_request.html",context)

#Supplier payment l2 - Pending Payment list
@login_required(login_url="/employee/login/")
def SupplierPaymentPendingPaymentList(request):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if u.profile.supplier_payment_user_type != 'L2':
                return JsonResponse({'Message': 'You are not allow to view this page'})               

        if request.method == 'GET':
                pending_list = SupplierPaymentRequest.objects.filter(
                        status = 'Approved1'
                ).values(
                        'id',   
                        'vpo__po_number',
                        'vpo__po_date',
                        'vpo__vpo__vendor__name',
                        'vpo__vpo__vendor__location',
                        'vpo__vpo__terms_of_payment',
                        'vpo__vpo__requester__first_name',
                        'vpo__vpo__requester__last_name',
                        'amount'
                )

                context['pending_list'] = pending_list

                if type == 'Sales':
                        return render(request,"Sales/SupplierPayment/pending_payment_list_l2.html",context)

#Supplier payment l2 - Pending Payment details
@login_required(login_url="/employee/login/")
def SupplierPaymentPendingPaymentDetails(request,request_id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if u.profile.supplier_payment_user_type != 'L2':
                return JsonResponse({'Message': 'You are not allow to view this page'})               

        if request.method == 'GET':
                request_details = SupplierPaymentRequest.objects.get(id=request_id)
                context['request_details'] = request_details

                vpo_lineitem = VendorPOLineitems.objects.filter(vpo=request_details.vpo.vpo)
                context['vpo'] = request_details.vpo
                context['vpo_lineitem'] = vpo_lineitem

                if type == 'Sales':
                        return render(request,"Sales/SupplierPayment/pending_payment_details_l2.html",context)

#Lavel1 Reject 
@login_required(login_url="/employee/login/")
def SupplierPaymentPendingApprovalReject2(request, request_id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name 

        if u.profile.supplier_payment_user_type != 'L2':
                return JsonResponse({'Message': 'You are not allow to view this page'})

        if request.method == 'POST':
                request_details = SupplierPaymentRequest.objects.get(id=request_id)
                request_details.status = 'Rejected2'
                request_details.save()

                return HttpResponseRedirect(reverse('supplier-payment-pending-payment-list-l2'))

#Label 2 Rejected list for buyer
@login_required(login_url="/employee/login/")
def SupplierPaymentLabel2RejectList(request):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name               

        if request.method == 'GET':
                request_list = SupplierPaymentRequest.objects.filter(
                        status = 'Rejected2',
                        requester = u
                ).values(
                        'id',   
                        'vpo__po_number',
                        'vpo__po_date',
                        'vpo__vpo__vendor__name',
                        'vpo__vpo__vendor__location',
                        'amount'
                )

                context['request_list'] = request_list
                return render(request,"Sourcing/SupplierPayment/label2_reject_list.html",context)

#Label 2 Add Payment information
@login_required(login_url="/employee/login/")
def SupplierPaymentPendingAddPaymentInfo(request,request_id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name               

        if u.profile.supplier_payment_user_type != 'L2':
                return JsonResponse({'Message': 'You are not allow to view this page'})

        if request.method == 'POST':
                request_details = SupplierPaymentRequest.objects.get(id=request_id)

                data = request.POST
                #if 1<2 :
                try:
                        myfile = request.FILES['supporting_document']
                        SupplierPaymentInfo.objects.create(
                                payment_request = request_details,
                                amount = data['amount'],
                                payment_by = u,
                                attachment1 = myfile
                        )

                        request_details.status = 'Payment_Done'
                        request_details.save()
                except:
                        pass

                return HttpResponseRedirect(reverse('supplier-payment-pending-payment-list-l2'))

#All Supplier Payment List
@login_required(login_url="/employee/login/")
def SupplierPaymentAllList(request):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name               

        if request.method == 'GET':
                if type == 'Sales':
                        payment_info = SupplierPaymentInfo.objects.all().values(
                                'payment_request__vpo__po_number',
                                'payment_request__vpo__vpo__vendor__name',
                                'payment_request__vpo__vpo__vendor_contact_person__name',
                                'amount',
                                'payment_by__first_name',
                                'payment_by__last_name',
                                'payment_date',
                                'payment_request__requester__first_name',
                                'payment_request__requester__last_name',
                                'attachment1'
                        )
                        context['payment_info'] = payment_info                
                        return render(request,"Sales/SupplierPayment/supplier_payment_all_list.html",context)

                if type == 'Sourcing':
                        payment_info = SupplierPaymentInfo.objects.filter(payment_request__requester=u).values(
                                'payment_request__vpo__po_number',
                                'payment_request__vpo__vpo__vendor__name',
                                'payment_request__vpo__vpo__vendor_contact_person__name',
                                'amount',
                                'payment_by__first_name',
                                'payment_by__last_name',
                                'payment_date',
                                'payment_request__requester__first_name',
                                'payment_request__requester__last_name',
                                'attachment1'
                        )
                        context['payment_info'] = payment_info                
                        return render(request,"Sourcing/SupplierPayment/supplier_payment_all_list.html",context)