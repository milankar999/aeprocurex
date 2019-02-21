from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from State.models import StateList


@login_required(login_url="/employee/login/")
def suppliers(request):
    context={}
    context['supplier'] = 'active'

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        supplier = SupplierProfile.objects.all()
        context['SupplierList'] = supplier
        state = StateList.objects.all()
        context['StateList'] = state
        
        if type == 'Sourcing':
                return render(request,"Sourcing/Supplier/supplier.html",context)


    if request.method == "POST":
        user = User.objects.get(username=request.user)
        data = request.POST
        if data['country'].upper() == 'INDIA':
            supplier_id = 'V9' + str(format(SupplierProfile.objects.count() + 1, '05d'))
        else:
            supplier_id = 'VI9' + str(format(SupplierProfile.objects.count() + 1, '05d'))

        if data['PaymentTerm'] == '':
            pt = 0
        else:
            pt=data['PaymentTerm']
        
        if data['advance'] == '':
            adv = 0
        else:
            adv = data['advance']
        ven = SupplierProfile.objects.create(id=supplier_id,name=data['name'],location=data['location'],address=data['address'],city=data['city'],state=data['state'],pin=data['pin'],country=data['country'],office_email1=data['officeemail1'],office_email2=data['officeemail2'],office_phone1=data['officephone1'],office_phone2=data['officephone2'],gst_number=data['GSTNo'],advance_persentage=adv,payment_term=pt,inco_term=data['IncoTerm'],created_by=user)
        if ven:
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                supplier = SupplierProfile.objects.all()
                context['SupplierList'] = supplier
                state = StateList.objects.all()
                context['StateList'] = state
                context['message'] = 'Successfully registered ' + data['name']
                context['message_type'] = 'success'
                if type == 'Sourcing':
                    return render(request,"Sourcing/Supplier/supplier.html",context)
        
        else:
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                supplier = SupplierProfile.objects.all()
                context['SupplierList'] = supplier
                state = StateList.objects.all()
                context['StateList'] = state
                context['message'] = 'Something went wrong'
                context['message_type'] = 'danger'
                if type == 'Sourcing':
                    return render(request,"Sourcing/Supplier/supplier.html",context)

@login_required(login_url="/employee/login/")
def supplier_details(request, id=None):
    context={}
    context['supplier'] = 'active'

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        supplier = SupplierProfile.objects.get(id=id)
        context['Supplier'] = supplier
        
        if type == 'Sourcing':
                return render(request,"Sourcing/Supplier/supplier_details.html",context)

@login_required(login_url="/employee/login/")
def supplier_edit(request, id=None):
    context={}
    context['supplier'] = 'active'
    user = User.objects.get(username=request.user)

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        supplier = SupplierProfile.objects.get(id=id)
        context['Supplier'] = supplier
        state = StateList.objects.all()
        context['StateList'] = state
        
        if type == 'Sourcing':
                return render(request,"Sourcing/Supplier/supplier_edit.html",context)

    if request.method=="POST":
        suppData = SupplierProfile.objects.get(id=id)
        data = request.POST

        if data['PaymentTerm'] == '':
            pt = 0
        else:
            pt=data['PaymentTerm']
        
        if data['advance'] == '':
            adv = 0
        else:
            adv = data['advance']

        suppData.name = data['name']
        suppData.location = data['location']
        suppData.address = data['address']
        suppData.city = data['city']
        suppData.state = data['state']
        suppData.pin = data['pin']
        suppData.country = data['country']
        suppData.office_email1 = data['officeemail1']
        suppData.office_email2 = data['officeemail2']
        suppData.office_phone1 = data['officephone1']
        suppData.office_phone2 = data['officephone2']
        suppData.gst_number = data['GSTNo']
        suppData.advance_persentage = adv
        suppData.payment_term = pt
        suppData.inco_term = data['IncoTerm']
        suppData.save()
        
        context['message'] = "Updated Successfully"
        context['message_type'] = 'success' 
        
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        supplier = SupplierProfile.objects.get(id=id)
        context['Supplier'] = supplier
        state = StateList.objects.all()
        context['StateList'] = state
        
        if type == 'Sourcing':
                return render(request,"Sourcing/Supplier/supplier_edit.html",context)

@login_required(login_url="/employee/login/")
def supplier_contact_person(request,id=None):
    context={}
    context['supplier'] = 'active'

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        ContactPerson = SupplierContactPerson.objects.filter(supplier_name__pk=id)
        context['ContactPerson'] = ContactPerson
        supplier = SupplierProfile.objects.get(id=id)
        context['SupplierName'] = supplier.name

        
        if type == 'Sourcing':
                return render(request,"Sourcing/Supplier/contact_person.html",context)

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        data = request.POST
        supplier = SupplierProfile.objects.get(id=id)
        contactperson_id =  id +'VP' + str(SupplierContactPerson.objects.count() + 1)
        cp = SupplierContactPerson.objects.create(id=contactperson_id,name=data['name'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],supplier_name=supplier,created_by=user)
        if cp:
                context['message'] = 'Successfully registered ' + data['name']
                context['message_type'] = 'success'
        else:
                context['message'] = 'Something went wrong'
                context['message_type'] = 'danger'

        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        ContactPerson = SupplierContactPerson.objects.filter(supplier_name__pk=id)
        context['ContactPerson'] = ContactPerson
        supplier = SupplierProfile.objects.get(id=id)
        context['SupplierName'] = supplier.name

        
        if type == 'Sourcing':
                return render(request,"Sourcing/Supplier/contact_person.html",context)


@login_required(login_url="/employee/login/")
def supplier_contact_person_edit(request,supp_id=None,person_id=None):
    context={}
    context['supplier'] = 'active'

    if request.method == "GET":
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        ContactPerson = SupplierContactPerson.objects.get(id=person_id)
        context['ContactPerson'] = ContactPerson


        if type == 'Sourcing':
                return render(request,"Sourcing/Supplier/contact_person_edit.html",context)

    if request.method == "POST":
        spData = SupplierContactPerson.objects.get(id=person_id)
        data = request.POST
        spData.name = data['name']
        spData.mobileNo1 = data['phone1']
        spData.mobileNo2 = data['phone2']
        spData.email1 = data['email1']
        spData.email2 = data['email2']
        spData.save()

        context['message'] = "Updated Successfully"
        context['message_type'] = 'success' 

        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name
        ContactPerson = SupplierContactPerson.objects.get(id=person_id)
        context['ContactPerson'] = ContactPerson


        if type == 'Sourcing':
                return render(request,"Sourcing/Supplier/contact_person_edit.html",context)