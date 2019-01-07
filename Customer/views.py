import csv, io 
import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,permission_required
from django.urls import reverse
from .models import *
from State.models import StateList


@login_required(login_url="/employee/login/")
def customers(request):
    context={}
    context['customer'] = 'active'

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        customer = CustomerProfile.objects.all()
        context['CustomerList'] = customer
        state = StateList.objects.all()
        context['StateList'] = state
        
        if type == 'CRM':
                return render(request,"CRM/Customer/customer.html",context)


    if request.method == "POST":
        user = User.objects.get(username=request.user)
        data = request.POST
        customer_id = 'C1' + str(format(CustomerProfile.objects.count() + 1, '04d'))
        cust = CustomerProfile.objects.create(
                id=customer_id,name=data['name'],
                location=data['location'],
                code=data['code'],
                address=data['address'],
                billing_address=data['billing_address'],
                shipping_address=data['shipping_address'],
                city=data['city'],
                state=data['state'],
                pin=data['pin'],
                country=data['country'],
                office_email1=data['officeemail1'],
                office_email2=data['officeemail2'],
                office_phone1=data['officephone1'],
                office_phone2=data['officephone2'],
                gst_number=data['GSTNo'],
                vendor_code=data['VendorCode'],
                payment_term=data['PaymentTerm'],
                inco_term=data['IncoTerm'],
                tax_type=data['tax_type'],
                created_by=user
        )
        if cust:
                u = User.objects.get(username=request.user)
                type = u.profile.type
                customer = CustomerProfile.objects.all()
                context['CustomerList'] = customer
                state = StateList.objects.all()
                context['StateList'] = state
                context['message'] = 'Successfully registered ' + data['name']
                context['message_type'] = 'success'
                if type == 'CRM':
                        return render(request,"CRM/Customer/customer.html",context)
        
        else:
                u = User.objects.get(username=request.user)
                type = u.profile.type
                customer = CustomerProfile.objects.all()
                context['CustomerList'] = customer
                state = StateList.objects.all()
                context['StateList'] = state
                context['message'] = 'Something went wrong'
                context['message_type'] = 'danger'
                if type == 'CRM':
                        return render(request,"CRM/Customer/customer.html",context)

@login_required(login_url="/employee/login/")
def customer_details(request, id=None):
    context={}
    context['customer'] = 'active'

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        customer = CustomerProfile.objects.get(id=id)
        context['Customer'] = customer
        
        if type == 'CRM':
                return render(request,"CRM/Customer/customer_details.html",context)

@login_required(login_url="/employee/login/")
def customer_edit(request, id=None):
    context={}
    context['customer'] = 'active'
    user = User.objects.get(username=request.user)

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        customer = CustomerProfile.objects.get(id=id)
        context['Customer'] = customer
        state = StateList.objects.all()
        context['StateList'] = state
        
        if type == 'CRM':
                return render(request,"CRM/Customer/customer_edit.html",context)

    if request.method=="POST":
        custData = CustomerProfile.objects.get(id=id)
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
        
        context['message'] = "Updated Successfully"
        context['message_type'] = 'success' 
        
        u = User.objects.get(username=request.user)
        type = u.profile.type
        customer = CustomerProfile.objects.get(id=id)
        context['Customer'] = customer
        state = StateList.objects.all()
        context['StateList'] = state
        
        if type == 'CRM':
                return render(request,"CRM/Customer/customer_edit.html",context)

@login_required(login_url="/employee/login/")
def contact_person(request,id=None):
    context={}
    context['customer'] = 'active'

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        ContactPerson = CustomerContactPerson.objects.filter(customer_name__pk=id)
        context['ContactPerson'] = ContactPerson
        customer = CustomerProfile.objects.get(id=id)
        context['CustomerName'] = customer.name

        
        if type == 'CRM':
                return render(request,"CRM/Customer/contact_person.html",context)

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        data = request.POST
        customer = CustomerProfile.objects.get(id=id)
        contactperson_id =  id +'P' + str(CustomerContactPerson.objects.count() + 1)
        cp = CustomerContactPerson.objects.create(id=contactperson_id,name=data['name'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],customer_name=customer,created_by=user)
        if cp:
                context['message'] = 'Successfully registered ' + data['name']
                context['message_type'] = 'success'
        else:
                context['message'] = 'Something went wrong'
                context['message_type'] = 'danger'

        u = User.objects.get(username=request.user)
        type = u.profile.type
        ContactPerson = CustomerContactPerson.objects.filter(customer_name__pk=id)
        context['ContactPerson'] = ContactPerson
        customer = CustomerProfile.objects.get(id=id)
        context['CustomerName'] = customer.name

        
        if type == 'CRM':
                return render(request,"CRM/Customer/contact_person.html",context)

@login_required(login_url="/employee/login/")
def contact_person_edit(request,cust_id=None,person_id=None):
    context={}
    context['customer'] = 'active'

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        ContactPerson = CustomerContactPerson.objects.get(id=person_id)
        context['ContactPerson'] = ContactPerson


        if type == 'CRM':
                return render(request,"CRM/Customer/contact_person_edit.html",context)

    if request.method == "POST":
        cpData = CustomerContactPerson.objects.get(id=person_id)
        data = request.POST
        cpData.name = data['name']
        cpData.mobileNo1 = data['phone1']
        cpData.mobileNo2 = data['phone2']
        cpData.email1 = data['email1']
        cpData.email2 = data['email2']
        cpData.save()

        context['message'] = "Updated Successfully"
        context['message_type'] = 'success' 

        u = User.objects.get(username=request.user)
        type = u.profile.type
        ContactPerson = CustomerContactPerson.objects.get(id=person_id)
        context['ContactPerson'] = ContactPerson


        if type == 'CRM':
                return render(request,"CRM/Customer/contact_person_edit.html",context)

@login_required(login_url="/employee/login/")
def enduser(request,id=None):
    context={}
    context['customer'] = 'active'

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        enduser = EndUser.objects.filter(customer_name__pk=id)
        context['EndUser'] = enduser
        customer = CustomerProfile.objects.get(id=id)
        context['CustomerName'] = customer.name

        
        if type == 'CRM':
                return render(request,"CRM/Customer/enduser.html",context)

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        data = request.POST
        customer = CustomerProfile.objects.get(id=id)
        enduser_id =  id +'D' + str(EndUser.objects.count() + 1)
        cp = EndUser.objects.create(id=enduser_id,user_name=data['name'],department_name = data['dept'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],customer_name=customer,created_by=user)
        if cp:
                context['message'] = 'Successfully registered ' + data['name']
                context['message_type'] = 'success'
        else:
                context['message'] = 'Something went wrong'
                context['message_type'] = 'danger'

        u = User.objects.get(username=request.user)
        type = u.profile.type
        user = EndUser.objects.filter(customer_name__pk=id)
        context['EndUser'] = user
        customer = CustomerProfile.objects.get(id=id)
        context['CustomerName'] = customer.name

        
        if type == 'CRM':
                return render(request,"CRM/Customer/enduser.html",context)

@login_required(login_url="/employee/login/")
def enduser_edit(request,cust_id=None,enduser_id=None):
    context={}
    context['customer'] = 'active'

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        enduser = EndUser.objects.get(id=enduser_id)
        context['EndUser'] = enduser


        if type == 'CRM':
                return render(request,"CRM/Customer/enduser_edit.html",context)

    if request.method == "POST":
        euData = EndUser.objects.get(id=enduser_id)
        data = request.POST
        euData.user_name = data['name']
        euData.department_name = data['dept']
        euData.mobileNo1 = data['phone1']
        euData.mobileNo2 = data['phone2']
        euData.email1 = data['email1']
        euData.email2 = data['email2']
        euData.save()

        context['message'] = "Updated Successfully"
        context['message_type'] = 'success' 

        u = User.objects.get(username=request.user)
        type = u.profile.type
        enduser = EndUser.objects.get(id=enduser_id)
        context['EndUser'] = enduser 

        if type == 'CRM':
                return render(request,"CRM/Customer/enduser_edit.html",context)

@permission_required('admin.can_add_log_entry')
def CustomerProfileUpload(request):
        template = "Admin/Customer/customer_profile_upload.html"
        prompt = {
                'order' : 'Order of CSV should be  id,name,location,code,address,city,state,pin,country,office_email1,office_email2,office_phone1,office_phone2,gst_number,vendor_code,payment_term,inco_term,tax_type,billing_address,shipping_address'
        }
        if request.method == "GET":
                return render(request,template,prompt)

        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.json'):
                messages.error(request,'this is not a csv file')
        
        data_set = csv_file.read()
        data = json.dumps(csv_file)
        
        #print(data)

        context = {}
        return render (request, template, context)