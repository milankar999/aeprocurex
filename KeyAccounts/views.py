from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from State.models import StateList
from RFP.models import *
import random
from django.conf import settings
from django.core import mail
from django.core.mail import send_mail, EmailMessage

@login_required(login_url="/employee/login/")
def enquiry_list(request):
    context={}
    context['key_accounts'] = 'active'
    user = User.objects.get(username=request.user)
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if type == 'Sourcing':
            if request.method == "GET":
                    rfp_list = RFP.objects.filter(rfp_keyaccounts_details__key_accounts_manager=user).values(
                        'rfp_no',
                        'customer__name',
                        'customer__location',
                        'customer_contact_person__name',
                        'rfp_creation_details__creation_date',
                        'rfp_assign1__assign_to1__first_name',
                        'enquiry_status',
                        'priority'
                    )
                    context['rfp_list'] = rfp_list
                    return render(request,"Sourcing/KeyAccounts/enquiry_list.html",context)

@login_required(login_url="/employee/login/")
def enquiry_lineitems(request,rfp_no=None):
    context={}
    context['key_accounts'] = 'active'
    user = User.objects.get(username=request.user)
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name

    if type == 'Sourcing':
            if request.method == "GET":
                    rfp_lineitems = RFPLineitem.objects.filter(rfp_no=rfp_no)
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
                        'rfp_creation_details__created_by__username'
                    )                  
                    context['rfp_no'] = rfp_no
                    context['lineitems'] = rfp_lineitems
                    context['rfp_details'] = rfp
                    users = User.objects.filter(profile__type='Sourcing')
                    context['users'] = users
                    keyaccounts = User.objects.all()
                    context['keyaccounts'] = keyaccounts
                    return render(request,"Sourcing/KeyAccounts/enquiry_lineitems.html",context)

            if request.method == "POST":
                    lineitemID = rfp_no + str(random.randint(100000,9999999))
                    data = request.POST
        
                    if data['gst'] == '':
                        gst = 0
                    else:
                        gst = data['gst']
        
                    if data['CLT'] == '':
                        CLT = 0
                    else:
                        CLT = data['CLT']

                    if data['target_price'] == '':
                        target_price = 0
                    else:
                        target_price = data['target_price']
                
        
                    RFPLineitem.objects.create(rfp_no=RFP.objects.get(rfp_no=rfp_no),lineitem_id=lineitemID,product_title = data['product_title'],description=data['description'],model=data['model'],brand=data['brand'],product_code=data['product_code'],part_no=data['part_no'],category = data['category'],hsn_code=data['hsn_code'],gst=gst,uom=data['uom'],quantity=data['quantity'],target_price=target_price,customer_lead_time=CLT,remarks=data['remarks'])
                    
                    #Sending Email Notification
                    rfp = RFP.objects.get(rfp_no=rfp_no)
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
                    '<h2><span style="color: #008000;">&nbsp; &nbsp; &nbsp; One New Lineitem Has Been added to RFP No - '+ rfp_no +'</span></h2>'\
                    '<p><span style="color: #0000ff;"><strong>Added By ' + request.user.first_name + ' ' + request.user.last_name + ' '\
                    '</strong></span><span style="color: #0000ff;">'\
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
                    msg = EmailMessage(subject=rfp_no, body=email_body, from_email = settings.DEFAULT_FROM_EMAIL,to = [email_receiver], bcc = ['sales.p@eprocurex.com','milan.kar@aeprocurex.com','prasannakumar.c@aeprocurex.com'])
                    msg.content_subtype = "html"  # Main content is now text/html
                    msg.send()
                    return HttpResponseRedirect(reverse('key_accounts_enquiry_lineitems',args=[rfp_no]))


@login_required(login_url="/employee/login/")
def enquiry_lineitems_edit(request, rfp_no=None, lineitem_id=None):
    context={}
    context['rfp'] = 'active'
    user = User.objects.get(username=request.user)
    u = User.objects.get(username=request.user)
    type = u.profile.type
    context['login_user_name'] = u.first_name + ' ' + u.last_name
    
    if request.method == "GET":        
        context['rfp_no'] = rfp_no

        lineitems = RFPLineitem.objects.get(lineitem_id=lineitem_id)
        context['lineitems'] = lineitems
        print(lineitems)
        if type == 'Sourcing':
                return render(request,"Sourcing/KeyAccounts/rfp_lineitem_edit.html",context)
 
    if request.method == "POST":
        lineitem = RFPLineitem.objects.get(lineitem_id=lineitem_id)
        data = request.POST
        
        if data['gst'] == '':
                gst = 0
        else:
                gst = data['gst']
        
        if data['CLT'] == '':
                CLT = 0
        else:
                CLT = data['CLT']

        if data['target_price'] == '':
                target_price = 0
        else:
                target_price = data['target_price']

        lineitem.product_title = data['product_title']
        lineitem.description=data['description']
        lineitem.model=data['model']
        lineitem.brand=data['brand']
        lineitem.product_code=data['product_code']
        lineitem.part_no=data['part_no']
        lineitem.category = data['category']
        lineitem.hsn_code=data['hsn_code']
        lineitem.gst=gst
        lineitem.uom=data['uom']
        lineitem.quantity=data['quantity']
        lineitem.target_price=target_price
        lineitem.customer_lead_time=CLT
        lineitem.remarks=data['remarks']
        lineitem.save()

        if type == 'Sourcing':
                return HttpResponseRedirect(reverse('key_accounts_enquiry_lineitems',args=[rfp_no]))