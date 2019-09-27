from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from Employee.models import *
from .models import *
from State.models import *
from Customer.models import *
from django.core.mail import send_mail, EmailMessage
from django.core import mail
import random
from django.conf import settings
import openpyxl

@login_required(login_url="/employee/login/")
def rfp_create(request):
        context={}
        context['rfp'] = 'active'

        if request.method == "GET":
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                customer = CustomerProfile.objects.all()
                context['CustomerList'] = customer
                state = StateList.objects.all()
                context['StateList'] = state
        
                if type == 'CRM':
                        return render(request,"CRM/RFP/rfp_create_1.html",context)

                if type == 'Sourcing':
                        return render(request,"Sourcing/RFP/rfp_create_1.html",context)

        if request.method == "POST":
                user = User.objects.get(username=request.user)
                data = request.POST
                customer_id = 'C1' + str(format(CustomerProfile.objects.count() + 1, '04d'))
                cust = CustomerProfile.objects.create(id=customer_id,name=data['name'],location=data['location'],code=data['code'],address=data['address'],city=data['city'],state=data['state'],pin=data['pin'],country=data['country'],office_email1=data['officeemail1'],office_email2=data['officeemail2'],office_phone1=data['officephone1'],office_phone2=data['officephone2'],gst_number=data['GSTNo'],vendor_code=data['VendorCode'],payment_term=data['PaymentTerm'],inco_term=data['IncoTerm'],created_by=user)
                if cust:
                        u = User.objects.get(username=request.user)
                        type = u.profile.type
                        context['login_user_name'] = u.first_name + ' ' + u.last_name
                        customer = CustomerProfile.objects.all()
                        context['CustomerList'] = customer
                        state = StateList.objects.all()
                        context['StateList'] = state
                        context['message'] = 'Successfully registered ' + data['name']
                        context['message_type'] = 'success'
                        if type == 'CRM':
                                return render(request,"CRM/RFP/rfp_create_1.html",context)
                        if type == 'Sourcing':
                                return render(request,"Sourcing/RFP/rfp_create_1.html",context)
        
                else:
                        u = User.objects.get(username=request.user)
                        type = u.profile.type
                        context['login_user_name'] = u.first_name + ' ' + u.last_name
                        customer = CustomerProfile.objects.all()
                        context['CustomerList'] = customer
                        state = StateList.objects.all()
                        context['StateList'] = state
                        context['message'] = 'Something went wrong'
                        context['message_type'] = 'danger'
                        if type == 'CRM':
                                return render(request,"CRM/RFP/rfp_create_1.html",context)

                        if type == 'Sourcing':
                                return render(request,"Sourcing/RFP/rfp_create_1.html",context)

@login_required(login_url="/employee/login/")
def contact_person(request, cust_id=None):
        context={}
        context['rfp'] = 'active'

        if request.method == "GET":
                user = User.objects.get(username=request.user)
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                ContactPerson = CustomerContactPerson.objects.filter(customer_name__pk=cust_id)
                context['ContactPerson'] = ContactPerson
                customer = CustomerProfile.objects.get(id=cust_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = cust_id

                if type == 'CRM':
                        return render(request,"CRM/RFP/rfp_create_2.html",context)
                if type == 'Sourcing':
                        return render(request,"Sourcing/RFP/rfp_create_2.html",context)

        if request.method == "POST":
                user = User.objects.get(username=request.user)
                data = request.POST
                customer = CustomerProfile.objects.get(id=cust_id)
                contactperson_id =  cust_id +'P' + str(CustomerContactPerson.objects.count() + 1)
                cp = CustomerContactPerson.objects.create(id=contactperson_id,name=data['name'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],customer_name=customer,created_by=user)
                if cp:
                        context['message'] = 'Successfully registered ' + data['name']
                        context['message_type'] = 'success'
                else:
                        context['message'] = 'Something went wrong'
                        context['message_type'] = 'danger'
      
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                ContactPerson = CustomerContactPerson.objects.filter(customer_name__pk=cust_id)
                context['ContactPerson'] = ContactPerson
                customer = CustomerProfile.objects.get(id=cust_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = cust_id


        
                if type == 'CRM':
                        return render(request,"CRM/RFP/rfp_create_2.html",context)

                if type == 'Sourcing':
                        return render(request,"Sourcing/RFP/rfp_create_2.html",context)

@login_required(login_url="/employee/login/")
def end_user(request, cust_id=None,contactperson_id=None):
        context={}
        context['rfp'] = 'active'

        if request.method == "GET":
                user = User.objects.get(username=request.user)
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                enduser = EndUser.objects.filter(customer_name__pk=cust_id)
                context['EndUser'] = enduser
                customer = CustomerProfile.objects.get(id=cust_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = cust_id
                context['ContactPersonID'] = contactperson_id

                if type == 'CRM':
                        return render(request,"CRM/RFP/rfp_create_3.html",context)

                if type == 'Sourcing':
                        return render(request,"Sourcing/RFP/rfp_create_3.html",context)

        if request.method == "POST":
                user = User.objects.get(username=request.user)
                data = request.POST
                customer = CustomerProfile.objects.get(id=cust_id)
                enduser_id =  cust_id +'D' + str(EndUser.objects.count() + 1)
                cp = EndUser.objects.create(id=enduser_id,user_name=data['name'],department_name = data['dept'],mobileNo1=data['phone1'],mobileNo2=data['phone2'],email1=data['email1'],email2=data['email2'],customer_name=customer,created_by=user)
                if cp:
                        context['message'] = 'Successfully registered ' + data['name']
                        context['message_type'] = 'success'
                else:
                        context['message'] = 'Something went wrong'
                        context['message_type'] = 'danger'

                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                user = EndUser.objects.filter(customer_name__pk=cust_id)
                context['EndUser'] = user
                customer = CustomerProfile.objects.get(id=cust_id)
                context['CustomerName'] = customer.name
                context['CustomerID'] = cust_id
                context['ContactPersonID'] = contactperson_id
        
                if type == 'CRM':
                        return render(request,"CRM/RFP/rfp_create_3.html",context)
                if type == 'Sourcing':
                        return render(request,"Sourcing/RFP/rfp_create_3.html",context)

@login_required(login_url="/employee/login/")
def processing(request, cust_id=None,contactperson_id=None,enduser_id=None):
        context={}
        context['rfp'] = 'active'

        if request.method == "GET":
                user = User.objects.get(username=request.user)
                u = User.objects.get(username=request.user)
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                type = u.profile.type
                enduser = EndUser.objects.filter(customer_name__pk=cust_id)
                context['EndUser'] = enduser
                customer = CustomerProfile.objects.get(id=cust_id)
                rfp_no = 'RFP' + customer.id + customer.code + str(RFP.objects.count()+1)
                customer = CustomerProfile.objects.get(id=cust_id)
                customer_contact_person = CustomerContactPerson.objects.get(id=contactperson_id)
        
                if enduser_id == 'none':
                        creation_details = RFPCreationDetail.objects.create(id=rfp_no+'C1',created_by=user)
                        new_rfp = RFP.objects.create(rfp_no=rfp_no,customer=customer,customer_contact_person=customer_contact_person,rfp_creation_details=creation_details)
                else:
                        end_user = EndUser.objects.get(id=enduser_id)
                        creation_details = RFPCreationDetail.objects.create(id=rfp_no+'C1',created_by=user)
                        new_rfp = RFP.objects.create(rfp_no=rfp_no,customer=customer,customer_contact_person=customer_contact_person,end_user=end_user,rfp_creation_details=creation_details)
                context['rfp_no'] = rfp_no

                if new_rfp:
                        if creation_details:
                                if type == 'CRM':
                                        return render(request,"CRM/RFP/process.html",context)

                                if type == 'Sourcing':
                                        return render(request,"Sourcing/RFP/process.html",context)

@login_required(login_url="/employee/login/")
def rfp_creation_inprogress(request):
        context={}
        context['rfp'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == "GET":
                if type == 'CRM':
                        rfp = RFP.objects.filter(enquiry_status='',rfp_creation_details__created_by=u).values(
                                'rfp_no',
                                'customer__name',
                                'customer__location',
                                'customer_contact_person__name',
                                'rfp_creation_details__creation_date'
                                )
                        context['rfp_list'] = rfp
                        return render(request,"CRM/RFP/creation_in_progress.html",context)  

                if type == 'Sourcing':
                        rfp = RFP.objects.filter(enquiry_status='',rfp_creation_details__created_by=u).values(
                                'rfp_no',
                                'customer__name',
                                'customer__location',
                                'customer_contact_person__name',
                                'rfp_creation_details__creation_date'
                                )
                        context['rfp_list'] = rfp
                        return render(request,"Sourcing/RFP/creation_in_progress.html",context)  
                     
@login_required(login_url="/employee/login/")
def product_selection(request, rfp_no=None):
        context={}
        context['rfp'] = 'active'
    
        if request.method == "GET":
                user = User.objects.get(username=request.user)
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                context['rfp_no'] = rfp_no

                lineitems = RFPLineitem.objects.filter(rfp_no__pk=rfp_no).order_by('creation_time')
                context['lineitems'] = lineitems

                if type == 'CRM':
                        return render(request,"CRM/RFP/product_selection.html",context)

                if type == 'Sourcing':
                        return render(request,"Sourcing/RFP/product_selection.html",context)
 
        if request.method == "POST":
                user = User.objects.get(username=request.user)
                u = User.objects.get(username=request.user)
                type = u.profile.type
                context['login_user_name'] = u.first_name + ' ' + u.last_name
                context['rfp_no'] = rfp_no
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
                
        
                rfp_lineitem = RFPLineitem.objects.create(rfp_no=RFP.objects.get(rfp_no=rfp_no),lineitem_id=lineitemID,product_title = data['product_title'],description=data['description'],model=data['model'],brand=data['brand'],product_code=data['product_code'],part_no=data['part_no'],category = data['category'],hsn_code=data['hsn_code'],gst=gst,uom=data['uom'],quantity=data['quantity'],target_price=target_price,customer_lead_time=CLT,remarks=data['remarks'])

                lineitems = RFPLineitem.objects.filter(rfp_no__pk=rfp_no)
                context['lineitems'] = lineitems

                if type == 'CRM':
                        return render(request,"CRM/RFP/product_selection.html",context)

                if type == 'Sourcing':
                        return render(request,"Sourcing/RFP/product_selection.html",context)

#Upload Product
@login_required(login_url="/employee/login/")
def upload_product(request, rfp_no=None):
        context={}
        context['rfp'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == "POST":
                try:
                        data_file = request.FILES['product_file']
                        wb = openpyxl.load_workbook(data_file)
                        worksheet = wb['ProductDetails']
                        for row in worksheet.iter_rows():
                                lineitemID = rfp_no + str(random.randint(100000,9999999))
                                try:
                                        RFPLineitem.objects.create(
                                                rfp_no=RFP.objects.get(rfp_no=rfp_no),
                                                lineitem_id=lineitemID,
                                                product_title = row[1].value,
                                                description=row[2].value,
                                                model=row[3].value,
                                                brand=row[4].value,
                                                product_code=row[5].value,
                                                part_no=row[6].value,
                                                category = row[7].value,
                                                hsn_code=row[8].value,
                                                gst=row[9].value,
                                                uom=row[10].value,
                                                quantity=row[11].value,
                                                target_price=row[12].value,
                                                customer_lead_time=row[14].value,
                                                remarks=row[13].value
                                                )   

                                except:
                                        pass      

                except:
                        pass
                return HttpResponseRedirect(reverse('product-selection',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def lineitem_edit(request, rfp_no=None, lineitem_id=None):
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
                if type == 'CRM':
                        return render(request,"CRM/RFP/rfp_lineitem_edit.html",context)
                if type == 'Sourcing':
                        return render(request,"Sourcing/RFP/rfp_lineitem_edit.html",context)
 
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

                if type == 'CRM':
                        return HttpResponseRedirect(reverse('product-selection',args=[rfp_no]))
                if type == 'Sourcing':
                        return HttpResponseRedirect(reverse('product-selection',args=[rfp_no]))

@login_required(login_url="/employee/login/")
def lineitem_delete(request, rfp_no=None, lineitem_id=None):
        context={}
        context['rfp'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == "POST":
                lineitem = RFPLineitem.objects.get(lineitem_id=lineitem_id)
                lineitem.delete()

                if type == 'CRM':
                        return HttpResponseRedirect(reverse('product-selection',args=[rfp_no]))

                if type == 'Sourcing':
                        return HttpResponseRedirect(reverse('product-selection',args=[rfp_no]))


@login_required(login_url="/employee/login/")
def rfp_generate(request, rfp_no=None):
        context={}
        context['rfp'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == "POST":
                rfp = RFP.objects.get(rfp_no=rfp_no)
                data = request.POST

                if data['rfp_type'] == 'PSP':
                        rfp_lineitem = RFPLineitem.objects.filter(rfp_no = rfp)

                        for item in rfp_lineitem:
                                if item.target_price == 0 :
                                        return(JsonResponse({'Message' : 'Please mention target price for all items as it is PSP'}))

                rfp.reference = data['rfp_reference']
                rfp.priority = data['priority']
                rfp.rfp_type = data['rfp_type']
                rfp.opportunity_status = 'Open'
                rfp.enquiry_status = 'Created'

                try:
                        rfp.document1 = request.FILES['supporting_document1']
                except:
                        pass
                
                if data['pf_charge'] == '':
                        pf_charge = 0
                else:
                        pf_charge = data['pf_charge']

                if data['freight_charge'] == '':
                        freight_charge = 0
                else:
                        freight_charge = data['freight_charge']
                
                rfp.pf_charges = pf_charge
                rfp.freight_charges = freight_charge
                rfp.save()

                #email_list = []
                #sales_team_email = Profile.objects.filter(type='Sales').values('user__email')
                #for email in sales_team_email:
                #        email_list.append(email['user__email']) 
                #print(email_list)

                lineitems = RFPLineitem.objects.filter(rfp_no=rfp)
                #Sending mail Notification
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
                '<p><span style="color: #0000ff;"><strong>A New Enquiry Has Been Created By :' + rfp.rfp_creation_details.created_by.first_name + ' ' + rfp.rfp_creation_details.created_by.last_name + ' | '\
                ' At : ' + str(rfp.rfp_creation_details.creation_date) + ' '\
                '</strong></span><span style="color: #0000ff;">'\
                '<p><span style="color: #0000ff;"><strong>RFP No : '+ rfp_no +'</strong></span></p>'\
                '<p><span style="color: #0000ff;"><strong>Enquiry Type : '+ data['rfp_type'] +'</strong></span></p>'\
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
                '<p><span style="color: #ff0000;">Please Assign this RFP to a sourcing Person</span></p>'\
                '</body>'
                #msg = EmailMessage(subject=rfp_no, body=email_body, from_email = settings.DEFAULT_FROM_EMAIL, to = email_list, bcc = ['milan.kar@aeprocurex.com'])
                #msg.content_subtype = "html"  # Main content is now text/html
                #msg.send()
        
                if type == 'CRM':
                        context['rfp_no'] = rfp_no
                        return render(request,"CRM/RFP/success.html",context)
        
                if type == 'Sourcing':
                        context['rfp_no'] = rfp_no
                        return render(request,"Sourcing/RFP/success.html",context)

@login_required(login_url="/employee/login/")
def rfp_approval_list(request):
        context={}
        context['rfp'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if type == 'Sales':
                if request.method == "GET":
                        rfp = RFP.objects.filter(opportunity_status='Open',enquiry_status='Created').values('rfp_no','customer__name','customer__location','customer_contact_person__name','rfp_creation_details__creation_date','priority','rfp_type')    
                        context['rfp_list'] = rfp
                        return render(request,"Sales/RFP/rfp_approval_list.html",context)

@login_required(login_url="/employee/login/")
def rfp_approval_lineitems(request, rfp_no=None):
        context={}
        context['rfp'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if type == 'Sales':
                if request.method == "GET":
                        rfp_lineitems = RFPLineitem.objects.filter(rfp_no=rfp_no).order_by('creation_time')
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
                                'rfp_type',
                                'rfp_creation_details__created_by__username',
                                'document1',
                                'pf_charges',
                                'freight_charges')                  
                        context['rfp_no'] = rfp_no
                        context['lineitems'] = rfp_lineitems
                        context['rfp_details'] = rfp
                        users = User.objects.filter(profile__type='Sourcing')
                        context['users'] = users
                        keyaccounts = User.objects.all()
                        context['keyaccounts'] = keyaccounts
                        return render(request,"Sales/RFP/rfp_approval_lineitems.html",context)

@login_required(login_url="/employee/login/")
def rfp_reject(request, rfp_no=None):
        context={}
        context['rfp'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if type == 'Sales':
                if request.method == "POST":
                        data = request.POST
                        rfp = RFP.objects.get(rfp_no=rfp_no)
                        rfp.rejection_reason = data['rejection']
                        rfp.enquiry_status = 'Reject'
                        rfp.save()
                    
                        #Sending mail Notification
                        email_receiver = rfp.rfp_creation_details.created_by.email
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
                        '<p><span style="color: #0000ff;"><strong>A RFP Been Rejected by ' + request.user.first_name + ' ' + request.user.last_name + ' '\
                        'At : ' + str(rfp.rfp_creation_details.creation_date) + ' '\
                        '</strong></span><span style="color: #0000ff;">'\
                        '<p><span style="color: #0000ff;"><strong>RFP No : '+ rfp_no +'</strong></span></p>'\
                        '<p><span style="color: #0000ff;"><strong>Rejection Reason : '+ data['rejection'] +'</strong></span></p>'\
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
                        '<p><span style="color: #ff0000;">Please Rectify this Enquiry</span></p>'\
                        '</body>'
                        msg = EmailMessage(subject=rfp_no, body=email_body, from_email = settings.DEFAULT_FROM_EMAIL,to = [email_receiver], bcc = ['sales.p@aeprocurex.com','milan.kar@aeprocurex.com'])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()

                        context['message'] = 'RFP No ' + rfp_no + ' has been rejected successfully'
                        return render(request,"Sales/RFP/success.html",context)

@login_required(login_url="/employee/login/")
def rfp_approve(request, rfp_no=None):
        context={}
        context['rfp'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if type == 'Sales':
                if request.method == "POST":
                        data = request.POST

                        key_instance = User.objects.get(username=data['keyPerson'])    
                        keyaccounts = RFPKeyAccountsDetail.objects.create(id=rfp_no+str(random.randint(1000,99999)),key_accounts_manager = key_instance)
                        assign1 = RFPAssign1.objects.create(id=rfp_no+str(random.randint(1000,99999)),assign_to1=User.objects.get(username=data['assign1']))
                        #if data['assign2'] != '' :
                        #        assign2 = RFPAssign2.objects.create(id=rfp_no+str(random.randint(1000,99999)),assign_to2=User.objects.get(username=data['assign2']))
                        #if data['assign3'] != '' :
                        #        assign3 = RFPAssign3.objects.create(id=rfp_no+str(random.randint(1000,99999)),assign_to3=User.objects.get(username=data['assign3']))
                        rfp = RFP.objects.get(rfp_no=rfp_no)
                        rfpapprovaldetail = RFPApprovalDetail.objects.create(id=rfp_no+str(random.randint(1000,99999)),approved_by=user)
                        rfp.enquiry_status = 'Approved'
                        rfp.rfp_approval_details = rfpapprovaldetail
                        rfp.rfp_keyaccounts_details = keyaccounts
                        rfp.rfp_assign1 = assign1
                        #if data['assign2'] != '' :
                        #        rfp.rfp_assign2 = assign2
                        #if data['assign3'] != '' :
                        #        rfp.rfp_assign3 = assign3
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
                        msg = EmailMessage(subject=rfp_no, body=email_body, from_email = settings.DEFAULT_FROM_EMAIL,to = [email_receiver])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()
                        context['message'] = 'RFP No ' + rfp_no + ' has been approved successfully'
                        return render(request,"Sales/RFP/success.html",context)


@login_required(login_url="/employee/login/")
def rfp_rejected_list(request):
        context={}
        context['rfp'] = 'active'
        user = User.objects.get(username=request.user)
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if type == 'CRM':
                if request.method == "GET":
                        rfp = RFP.objects.filter(opportunity_status='Open',enquiry_status='Reject',rfp_creation_details__created_by=user).values(
                                'rfp_no',
                                'customer__name',
                                'customer__location',
                                'customer_contact_person__name',
                                'rfp_creation_details__creation_date',
                                'priority'
                                )    
                        context['rfp_list'] = rfp
                        print(rfp)
                        return render(request,"CRM/RFP/rfp_rejected_list.html",context)
