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
from django.db.models import F, DurationField, ExpressionWrapper
import textwrap
import datetime
import os
from django.views.static import serve
from django.http import FileResponse
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
from django.core import mail
from django.conf import settings
from django.db.models import Count
from datetime import timedelta, datetime
import pytz


@login_required(login_url="/employee/login/")
def enquiry_list(request):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        enquiry = RFP.objects.all().values(
            'rfp_no',
            'rfp_creation_details__creation_date',
            'customer__name',
            'customer__location',
            'customer_contact_person__name',
            'rfp_type',
            'rfp_creation_details__created_by__username',
            'rfp_assign1__assign_to1__username',
            'opportunity_status',
            'enquiry_status').order_by('-rfp_creation_details__creation_date')
        
        context['enquiry_list'] = enquiry

        if type == 'Sales':
            return render(request,"Sales/EnquiryTracker/enquiry_list.html",context)
        
        if type == 'CRM':
            return render(request,"CRM/EnquiryTracker/enquiry_list.html",context)
        
@login_required(login_url="/employee/login/")
def pending_enquiry_list(request):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        enquiry = RFP.objects.filter(Q(enquiry_status='Created') | Q(enquiry_status='Approved') | Q(enquiry_status='Sourcing_Completed') | Q(enquiry_status='COQ Done')).values(
            'rfp_no',
            'rfp_creation_details__creation_date',
            'customer__name',
            'customer__location',
            'customer_contact_person__name',
            'rfp_type',
            'rfp_creation_details__created_by__username',
            'rfp_assign1__assign_to1__username',
            'opportunity_status',
            'enquiry_status',
            'current_sourcing_status',
            'up_time').order_by('-rfp_creation_details__creation_date')
        
        utc=pytz.UTC
        for item in enquiry:
            diff = utc.localize(datetime.now()) - item['rfp_creation_details__creation_date']
            hrs = round((((diff.days) * 24) + (diff.seconds/3600)),2)
            item['up_time'] = hrs


        context['enquiry_list'] = enquiry

        if type == 'Sales':
            return render(request,"Sales/EnquiryTracker/pending_enquiry_list.html",context)

        if type == 'CRM':
            return render(request,"CRM/EnquiryTracker/pending_enquiry_list.html",context)

@login_required(login_url="/employee/login/")
def lineitem_list(request):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        lineitem_list = RFPLineitem.objects.all().values(
            'rfp_no__rfp_no',
            'rfp_no__rfp_creation_details__creation_date',
            'rfp_no__rfp_type',
            'rfp_no__enquiry_status',
            'lineitem_id',
            'product_title',
            'description',
            'model',
            'brand',
            'product_code',
            'part_no',
            'quantity',
            'uom',
            'rfp_no__customer__name',
            'rfp_no__customer__location',
            'rfp_no__rfp_keyaccounts_details__key_accounts_manager__username').order_by('-rfp_no__rfp_creation_details__creation_date')
        

        context['lineitem_list'] = lineitem_list

        if type == 'Sales':
            return render(request,"Sales/EnquiryTracker/lineitem_list.html",context)

        if type == 'CRM':
            return render(request,"CRM/EnquiryTracker/lineitem_list.html",context)

#RFP Details
@login_required(login_url="/employee/login/")
def rfp_lineitem(request,rfp_no=None):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        rfp_lineitems = RFPLineitem.objects.filter(rfp_no=RFP.objects.get(rfp_no=rfp_no)).values(
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
            'quantity')
        rfp = RFP.objects.filter(rfp_no=rfp_no).values(
                                'customer__name',
                                'customer__location',
                                'customer_contact_person__name',
                                'customer_contact_person__mobileNo1',
                                'customer_contact_person__email1',
                                'end_user__user_name',
                                'end_user__department_name',
                                'end_user__mobileNo1',
                                'end_user__email1',
                                'rfp_creation_details__creation_date',
                                'priority',
                                'reference',
                                'enquiry_status',
                                'rfp_type',
                                'rfp_creation_details__created_by__username',
                                'document1',
                                'document2',
                                'document3',
                                'document4',
                                'document5')               
        context['rfp_details'] = rfp
        context['rfp_lineitems'] = rfp_lineitems
        context['rfp_no'] = rfp_no

        context['rfp_status'] = rfp[0]['enquiry_status']

        users = User.objects.filter(profile__type='Sourcing')
        context['users'] = users
        keyaccounts = User.objects.all()
        context['keyaccounts'] = keyaccounts

        rfp_status_list = RFPStatus.objects.filter(rfp = RFP.objects.get(rfp_no=rfp_no))
        context['rfp_status_list'] = rfp_status_list

        if type == 'Sales':
            return render(request,"Sales/EnquiryTracker/rfp_lineitems.html",context)

        if type == 'CRM':
            return render(request,"CRM/EnquiryTracker/rfp_lineitems.html",context)

    if request.method == 'POST':
        data = request.POST
        rfp = RFP.objects.get(rfp_no=rfp_no)
        rfp.current_sourcing_status = data['status']
        rfp.save()

        RFPStatus.objects.create(
            rfp = rfp,
            status = data['status'],
            updated_by = u
            )

        return HttpResponseRedirect(reverse('tracker_rfp_lineitem',args=[rfp_no]))

#RFP Details
@login_required(login_url="/employee/login/")
def rfp_mark_duplicate(request,rfp_no=None):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "POST":
        rfp = RFP.objects.get(rfp_no = rfp_no)

        if rfp.enquiry_status != "Quoted":
            rfp.enquiry_status = 'Duplicate'
            rfp.opportunity_status = 'Duplicate'
            rfp.save()

            return HttpResponseRedirect(reverse('pending_enquiry_list'))
        
        else:
            context['error'] = "This is Already Quoted , Cannot be mark as Duplicate"
            return render(request,"Sales/error.html",context)

#RFP Details
@login_required(login_url="/employee/login/")
def rfp_mark_closed(request,rfp_no=None):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "POST":
        rfp = RFP.objects.get(rfp_no = rfp_no)

        if rfp.enquiry_status != "Quoted":
            rfp.enquiry_status = 'Closed'
            rfp.opportunity_status = 'Closed'
            rfp.save()

            return HttpResponseRedirect(reverse('pending_enquiry_list'))
        
        else:
            context['error'] = "This is Already Quoted , Cannot be mark as Duplicate"
            return render(request,"Sales/error.html",context)

#RFP Reassign
@login_required(login_url="/employee/login/")
def rfp_reassign(request,rfp_no=None):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "POST":
        data = request.POST
        rfp = RFP.objects.get(rfp_no = rfp_no)

        assign1 = RFPAssign1.objects.create(id=rfp_no+str(random.randint(1000,99999)),assign_to1=User.objects.get(username=data['assign1']))
        rfp.rfp_assign1 = assign1
        
        key_instance = User.objects.get(username=data['keyPerson'])    
        keyaccounts = RFPKeyAccountsDetail.objects.create(id=rfp_no+str(random.randint(1000,99999)),key_accounts_manager = key_instance)
        rfp.rfp_keyaccounts_details = keyaccounts

        rfpapprovaldetail = RFPApprovalDetail.objects.create(id=rfp_no+str(random.randint(1000,99999)),approved_by=u)
        rfp.rfp_approval_details = rfpapprovaldetail

        rfp.save()

        #Sending mail Notification
        email_receiver = rfp.rfp_assign1.assign_to1.email
        lineitems = RFPLineitem.objects.filter(rfp_no=rfp)
        email_body = '<head>'\
        '<style>'\
        'table {'\
        'width:100%;'\
        '}'\
        'table, th, td {'\
        'border: 1px solid black;'\
        'border-collapse: collapse;'\
        '}'\
        'th, td {'\
        'padding: 15px;'\
        'text-align: left;'\
        '}'\
        'table#t01 tr:nth-child(even) {'\
        'background-color: #eee;'\
        '}'\
        'table#t01 tr:nth-child(odd) {'\
        'background-color: #fff;'\
        '}'\
        'table#t01 th {'\
        'background-color: #1E2DFF;'\
        'color: white;'\
        '}'\
        '</style>'\
        '</head>'\
        '<body>'\
        '<h1 style="text-align: center;"><span style="color: #0000ff;"><strong>AEPROCUREX ERP</strong></span></h1>'\
        '<h2><span style="color: #008000;">Hello, ' + rfp.rfp_assign1.assign_to1.first_name + ' ' + rfp.rfp_assign1.assign_to1.last_name + '</span></h2>'\
        '<h2><span style="color: #008000;">&nbsp; &nbsp; &nbsp; One New RFP Has Been Assigned to You, Please Complete the Sourcing Earliest</span></h2>'\
        '<p><span style="color: #0000ff;"><strong>Assigned By ' + request.user.first_name + ' ' + request.user.last_name + ' '\
        '</strong></span><span style="color: #0000ff;">'\
        '<p><span style="color: #0000ff;"><strong>RFP No : '+ rfp_no +'</strong></span></p>'\
        '<p><span style="color: #0000ff;"><strong>Customer : '+ rfp.customer.name +'</strong></span></p>'\
        '<p><span style="color: #0000ff;"><strong>Requester : '+ rfp.customer_contact_person.name +'</strong></span></p>'\
        '<table id="t01">'\
        '<tr>'\
        '<th align="Centre">Sl #</th>'\
        '<th align="Centre">Product Title</th>'\
        '<th align="Centre">Description</th>' \
        '<th align="Centre">Quantity</th>'\
        '<th align="Centre">UOM</th>'\
        '</tr>'
        i = 1

        for items in lineitems:
            email_body = email_body + '<tr>'\
                '<td>'+ str(i) +'</td>'\
                '<td>'+ items.product_title +'</td>'\
                '<td>'+ items.description +'</td>'\
                '<td>'+ str(items.quantity) +'</td>'\
                '<td>'+ items.uom +'</td>'\
                '</tr>'
            i = i + 1
        email_body = email_body + '</table>'\
        '</body>'

        msg = EmailMessage(subject=rfp_no, body=email_body, from_email = settings.DEFAULT_FROM_EMAIL,to = [email_receiver], bcc = ['crm.p@aeprocurex.com','sales.p@aeprocurex.com','milan.kar@aeprocurex.com'])
        msg.content_subtype = "html"  # Main content is now text/html
        try:
            msg.send()
        except:
            pass

        return HttpResponseRedirect(reverse('pending_enquiry_list'))

#Pending Enquiry Slider
@login_required(login_url="/employee/login/")
def pending_enquiry_slider(request):
    context={}
    context['enquiry_tracker'] = 'active'
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
        
    if request.method == "GET":
        enquiry = RFP.objects.filter(Q(enquiry_status='Approved') | Q(enquiry_status='Sourcing_Completed') | Q(enquiry_status='COQ Done')).values(
            'rfp_no',
            'rfp_creation_details__creation_date',
            'customer__name',
            'customer__location',
            'customer_contact_person__name',
            'rfp_type',
            'rfp_creation_details__created_by__username',
            'rfp_assign1__assign_to1__username',
            'opportunity_status',
            'enquiry_status',
            'current_sourcing_status',
            'up_time').order_by('rfp_assign1__assign_to1__username')
        
        utc=pytz.UTC
        for item in enquiry:
            diff = utc.localize(datetime.now()) - item['rfp_creation_details__creation_date']
            hrs = round((((diff.days) * 24) + (diff.seconds/3600)),2)
            item['up_time'] = hrs

        enquiry_counter = RFP.objects.filter(Q(enquiry_status='Approved') | Q(enquiry_status='Sourcing_Completed') | Q(enquiry_status='COQ Done')).values(
            'rfp_assign1__assign_to1__first_name',
            'rfp_assign1__assign_to1__last_name',
            'rfp_assign1__assign_to1__username').annotate(count=Count('rfp_assign1__assign_to1__username'))
        
        pending_enquiry = RFP.objects.filter(Q(enquiry_status='Approved') | Q(enquiry_status='Sourcing_Completed') | Q(enquiry_status='COQ Done')).values(
            'rfp_assign1__assign_to1__username',
            'rfp_no',
            'rfp_creation_details__creation_date'       
        ).order_by('rfp_assign1__assign_to1__username')

        pending_lineitem = RFPLineitem.objects.filter(Q(rfp_no__enquiry_status='Approved') | Q(rfp_no__enquiry_status='Sourcing_Completed') | Q(rfp_no__enquiry_status='COQ Done')).values(
            'rfp_no__rfp_no',
            'product_title',
            'rfp_no__rfp_assign1__assign_to1__username'
        )

        time = RFP.objects.filter(Q(enquiry_status='Approved') | Q(enquiry_status='Sourcing_Completed') | Q(enquiry_status='COQ Done')).count()
        total_time = ((time * 7000) + 7000) * 2

        total_pending = 0
        for item in enquiry_counter:
            total_pending = total_pending + item['count']
        
        context['total_pending'] = total_pending

        context['total_time'] = total_time
        context['enquiry_list'] = enquiry
        context['enquiry_counter'] = enquiry_counter
        context['pending_enquiry'] = pending_enquiry
        context['pending_lineitem'] = pending_lineitem

        if type == 'Sales':
            return render(request,"Sales/EnquiryTracker/pending_enquiry_slider.html",context)

