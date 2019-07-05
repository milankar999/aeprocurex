from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from POForVendor.models import *
from django.core.mail import send_mail, EmailMessage
from django.core import mail
from django.conf import settings
from django.db.models import Q

host_name = 'http://localhost:8086/'
email_string_header = '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">'\
        '<head>'\
        '<meta charset="utf-8"> <!-- utf-8 works for most cases -->'\
        '<meta name="viewport" content="width=device-width">'\
        '<meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->'\
        '<meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->'\
        '<title></title> <!-- The title tag shows in email notifications, like Android 4.4. -->'\
        '<link href="https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700" rel="stylesheet">'\
        '<!-- CSS Reset : BEGIN -->'\
        '<style>'\
        'html,'\
        'body {'\
        'margin: 0 auto !important;'\
        'padding: 0 !important;'\
        'height: 100% !important;'\
        'width: 100% !important;'\
        'background: #f1f1f1;'\
        '}'\
        '/* What it does: Stops email clients resizing small text. */'\
        '* {'\
        '-ms-text-size-adjust: 100%;'\
        '-webkit-text-size-adjust: 100%;'\
        '}'\
        '/* What it does: Centers email on Android 4.4 */'\
        'div[style*="margin: 16px 0"] {'\
        'margin: 0 !important;'\
        '}'\
        '/* What it does: Stops Outlook from adding extra spacing to tables. */'\
        'table,'\
        'td {'\
        'mso-table-lspace: 0pt !important;'\
        'mso-table-rspace: 0pt !important;'\
        '}'\
        '/* What it does: Fixes webkit padding issue. */'\
        'table {'\
        'border-spacing: 0 !important;'\
        'border-collapse: collapse !important;'\
        'table-layout: fixed !important;'\
        'margin: 0 auto !important;'\
        '}'\
        '/* What it does: Uses a better rendering method when resizing images in IE. */'\
        'img {'\
        '-ms-interpolation-mode:bicubic;'\
        '}'\
        '/* What it does: Prevents Windows 10 Mail from underlining links despite inline CSS. Styles for underlined links should be inline. */'\
        'a {'\
        'text-decoration: none;'\
        '}'\
        '/* What it does: A work-around for email clients meddling in triggered links. */'\
        '*[x-apple-data-detectors],  /* iOS */'\
        '.unstyle-auto-detected-links *,'\
        '.aBn {'\
        'border-bottom: 0 !important;'\
        'cursor: default !important;'\
        'color: inherit !important;'\
        'text-decoration: none !important;'\
        'font-size: inherit !important;'\
        'font-family: inherit !important;'\
        'font-weight: inherit !important;'\
        'line-height: inherit !important;'\
        '}'\
        '/* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */'\
        '.a6S {'\
        'display: none !important;'\
        'opacity: 0.01 !important;'\
        '}'\
        '/* What it does: Prevents Gmail from changing the text color in conversation threads. */'\
        '.im {'\
        'color: inherit !important;'\
        '}'\
        '/* If the above doesnt work, add a .g-img class to any image in question. */'\
        'img.g-img + div {'\
        'display: none !important;'\
        '}'\
        '/* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */'\
        '/* Create one of these media queries for each additional viewport size youd like to fix */'\
        '/* iPhone 4, 4S, 5, 5S, 5C, and 5SE */'\
        '@media only screen and (min-device-width: 320px) and (max-device-width: 374px) {'\
        'u ~ div .email-container {'\
        'min-width: 320px !important;'\
        '}'\
        '}'\
        '/* iPhone 6, 6S, 7, 8, and X */'\
        '@media only screen and (min-device-width: 375px) and (max-device-width: 413px) {'\
        'u ~ div .email-container {'\
        'min-width: 375px !important;'\
        '}'\
        '}'\
        '/* iPhone 6+, 7+, and 8+ */'\
        '@media only screen and (min-device-width: 414px) {'\
        'u ~ div .email-container {'\
        'min-width: 414px !important;'\
        '}'\
        '}'\
        '</style>'\
        '<!-- CSS Reset : END -->'\
        '<!-- Progressive Enhancements : BEGIN -->'\
        '<style>'\
        '.primary{'\
	'background: #0d0cb5;'\
        '}'\
        '.bg_white{'\
	'background: #ffffff;'\
        '}'\
        '.bg_light{'\
	'background: #fafafa;'\
        '}'\
        '.bg_black{'\
	'background: #000000;'\
        '}'\
        '.bg_dark{'\
	'background: rgba(0,0,0,.8);'\
        '}'\
        '.email-section{'\
	'padding:2.5em;'\
        '}'\
        '/*BUTTON*/'\
        '.btn{'\
	'padding: 5px 15px;'\
	'display: inline-block;'\
        '}'\
        '.btn.btn-primary{'\
	'border-radius: 5px;'\
	'background: #0d0cb5;'\
	'color: #ffffff;'\
        '}'\
        '.btn.btn-white{'\
	'border-radius: 5px;'\
	'background: #ffffff;'\
	'color: #000000;'\
        '}'\
        '.btn.btn-white-outline{'\
	'border-radius: 5px;'\
	'background: transparent;'\
	'border: 1px solid #fff;'\
	'color: #fff;'\
        '}'\
        'h1,h2,h3,h4,h5,h6{'\
	'font-family: "Poppins", sans-serif;'\
	'color: #000000;'\
	'margin-top: 0;'\
        '}'\
        'body{'\
	'font-family: "Poppins", sans-serif;'\
	'font-weight: 400;'\
	'font-size: 15px;'\
	'line-height: 1.8;'\
	'color: rgba(0,0,0,.4);'\
        '}'\
        'a{'\
	'color: #0d0cb5;'\
        '}'\
        'table{'\
        '}'\
        '/*LOGO*/'\
        '.logo h1{'\
	'margin: 0;'\
        '}'\
        '.logo h1 a{'\
	'color: #000000;'\
	'font-size: 20px;'\
	'font-weight: 700;'\
	'text-transform: uppercase;'\
	'font-family: "Poppins", sans-serif;'\
        '}'\
        '.navigation{'\
	'padding: 0;'\
        '}'\
        '.navigation li{'\
	'list-style: none;'\
	'display: inline-block;'\
	'margin-left: 5px;'\
	'font-size: 13px;'\
	'font-weight: 500;'\
        '}'\
        '.navigation li a{'\
	'color: rgba(0,0,0,.4);'\
        '}'\
        '/*HERO*/'\
        '.hero{'\
	'position: relative;'\
	'z-index: 0;'\
        '}'\
        '.hero .overlay{'\
	'position: absolute;'\
	'top: 0;'\
	'left: 0;'\
	'right: 0;'\
	'bottom: 0;'\
	'content: '';'\
	'width: 100%;'\
	'background: #000000;'\
	'z-index: -1;'\
	'opacity: .3;'\
        '}'\
        '.hero .icon{'\
        '}'\
        '.hero .icon a{'\
	'display: block;'\
	'width: 60px;'\
	'margin: 0 auto;'\
        '}'\
        '.hero .text{'\
	'color: rgba(255,255,255,.8);'\
        '}'\
        '.hero .text h2{'\
	'color: #ffffff;'\
	'font-size: 30px;'\
	'margin-bottom: 0;'\
        '}'\
        '/*HEADING SECTION*/'\
        '.heading-section{'\
        '}'\
        '.heading-section h2{'\
	'color: #000000;'\
	'font-size: 20px;'\
	'margin-top: 0;'\
	'line-height: 1.4;'\
	'font-weight: 700;'\
	'text-transform: uppercase;'\
        '}'\
        '.heading-section .subheading{'\
	'margin-bottom: 20px !important;'\
	'display: inline-block;'\
	'font-size: 13px;'\
	'text-transform: uppercase;'\
	'letter-spacing: 2px;'\
	'color: rgba(0,0,0,.4);'\
	'position: relative;'\
        '}'\
        '.heading-section .subheading::after{'\
	'position: absolute;'\
	'left: 0;'\
	'right: 0;'\
	'bottom: -10px;'\
	'content: '';'\
	'width: 100%;'\
	'height: 2px;'\
	'background: #0d0cb5;'\
	'margin: 0 auto;'\
        '}'\
        '.heading-section-white{'\
	'color: rgba(255,255,255,.8);'\
        '}'\
        '.heading-section-white h2{'\
	'font-family: '\
	'line-height: 1;'\
	'padding-bottom: 0;'\
        '}'\
        '.heading-section-white h2{'\
	'color: #ffffff;'\
        '}'\
        '.heading-section-white .subheading{'\
	'margin-bottom: 0;'\
	'display: inline-block;'\
	'font-size: 13px;'\
	'text-transform: uppercase;'\
	'letter-spacing: 2px;'\
	'color: rgba(255,255,255,.4);'\
        '}'\
        '.icon{'\
	'text-align: center;'\
        '}'\
        '.icon img{'\
        '}'\
        '/*SERVICES*/'\
        '.services{'\
	'background: rgba(0,0,0,.03);'\
        '}'\
        '.text-services{'\
	'padding: 10px 10px 0; '\
	'text-align: center;'\
        '}'\
        '.text-services h3{'\
	'font-size: 16px;'\
	'font-weight: 600;'\
        '}'\
        '.services-list{'\
	'padding: 0;'\
	'margin: 0 0 20px 0;'\
	'width: 100%;'\
	'float: left;'\
        '}'\
        '.services-list img{'\
	'float: left;'\
        '}'\
        '.services-list .text{'\
	'width: calc(100% - 60px);'\
	'float: right;'\
        '}'\
        '.services-list h3{'\
	'margin-top: 0;'\
	'margin-bottom: 0;'\
        '}'\
        '.services-list p{'\
	'margin: 0;'\
        '}'\
        '/*BLOG*/'\
        '.text-services .meta{'\
	'text-transform: uppercase;'\
	'font-size: 14px;'\
        '}'\
        '/*TESTIMONY*/'\
        '.text-testimony .name{'\
	'margin: 0;'\
        '}'\
        '.text-testimony .position{'\
	'color: rgba(0,0,0,.3);'\
        '}'\
        '/*VIDEO*/'\
        '.img{'\
	'width: 100%;'\
	'height: auto;'\
	'position: relative;'\
        '}'\
        '.img .icon{'\
	'position: absolute;'\
	'top: 50%;'\
	'left: 0;'\
	'right: 0;'\
	'bottom: 0;'\
	'margin-top: -25px;'\
        '}'\
        '.img .icon a{'\
	'display: block;'\
	'width: 60px;'\
	'position: absolute;'\
	'top: 0;'\
	'left: 50%;'\
	'margin-left: -25px;'\
        '}'\
        '/*COUNTER*/'\
        '.counter{'\
	'width: 100%;'\
	'position: relative;'\
	'z-index: 0;'\
        '}'\
        '.counter .overlay{'\
	'position: absolute;'\
	'top: 0;'\
	'left: 0;'\
	'right: 0;'\
	'bottom: 0;'\
	'content: '';'\
	'width: 100%;'\
	'background: #000000;'\
	'z-index: -1;'\
	'opacity: .3;'\
        '}'\
        '.counter-text{'\
	'text-align: center;'\
        '}'\
        '.counter-text .num{'\
	'display: block;'\
	'color: #ffffff;'\
	'font-size: 34px;'\
	'font-weight: 700;'\
        '}'\
        '.counter-text .name{'\
	'display: block;'\
	'color: rgba(255,255,255,.9);'\
	'font-size: 13px;'\
        '}'\
        '/*FOOTER*/'\
        '.footer{'\
	'color: rgba(255,255,255,.5);'\
        '}'\
        '.footer .heading{'\
	'color: #ffffff;'\
	'font-size: 20px;'\
        '}'\
        '.footer ul{'\
	'margin: 0;'\
	'padding: 0;'\
        '}'\
        '.footer ul li{'\
	'list-style: none;'\
	'margin-bottom: 10px;'\
        '}'\
        '.footer ul li a{'\
	'color: rgba(255,255,255,1);'\
        '}'\
        '@media screen and (max-width: 500px) {'\
	'.icon{'\
	'text-align: left;'\
	'}'\
	'.text-services{'\
	'	padding-left: 0;'\
	'	padding-right: 20px;'\
	'	text-align: left;'\
	'}'\
        '}'\
        '</style>'\
        '</head>'\
        '<body width="100%" style="margin: 0; padding: 0 !important; mso-line-height-rule: exactly; background-color: #222222;">'\
	'<center style="width: 100%; background-color: #f1f1f1;">'\
        '<div style="display: none; font-size: 1px;max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">'\
        '&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;'\
        '</div>'\
        '<div style="max-width: 600px; margin: 0 auto;" class="email-container">'\
    	'<!-- BEGIN BODY -->'\
        '<table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">  '\
	'<!-- end tr -->'

email_string_footer = '<tr><hr></tr><tr>'\
	'<td class="primary email-section" style="text-align:center;">'\
	'  	<div class="heading-section heading-section-white">'\
	'	           	<p>A Process Flow Control System Managed by Aeprocurex</p>'\
	'	           	<p><a href='+ host_name +' class="btn btn-white-outline">MINI ERP HOME PAGE</a></p>'\
	'	       	</div>'\
	'	    </td>'\
	'	</tr><!-- end: tr -->'\
	'</table>     '\
        '<table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">'\
      	'<tr>'\
        '  <td valign="middle" class="bg_black footer email-section">'\
        '    <table>'\
        '    	<tr>'\
	'				<label>&copy; Aeprocurex Sourcing Private Limited</label>'\
        '      	</tr>'\
        '    </table>'\
        '  </td>'\
        '</tr><!-- end: tr -->'\
        '</table>'\
        '</div>'\
        '</center>'\
        '</body>'\
        '</html>'

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
                        sp = SupplierPaymentRequest.objects.create(
                            vpo = vpo,
                            amount = float(data['amount']),
                            notes = data['note'],
                            requester = u,
                            attachment1 = myfile
                        )

                except:
                        sp = SupplierPaymentRequest.objects.create(
                            vpo = vpo,
                            amount = float(data['amount']),
                            notes = data['note'],
                            requester = u
                        )
                request_heading = '<tr>'\
		        '<td class="bg_white">'\
		        '<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">'\
		        '<tr>'\
		        '<td class="bg_light email-section" style="width: 100%;">'\
		        '<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
		        '<tr>'\
			'<div class="heading-section">'\
			'<h2>Supplier Payment Request</h2>'\
			'<p>A Supplier Payment Request bas Been Created By '+ u.first_name + ' ' + u.last_name +', Waiting for your approval</p>'\
			'<p><a href="'+ host_name + 'supplier_payment/payment_request/pending_approval_list_1/'+ str(sp.id) +'/details/" class="btn btn-primary">Approve Now</a></p>'\
			'</div>	'\
                        '</tr>'\
                        '</table>'\
                      	'</td>'\
                        '</tr>'\
		        '</table>'\
		        '</td>'\
		        '</tr>'
                
                request_details = '<tr>'\
			'<td valign="top" class="bg_white" style="padding: 1em 2.5em;">'\
			'	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
			'		<tr>'\
			'			<td width="40%" class="logo" style="text-align: left;">'\
			'				<lavel>Supplier : '+ vpo.vpo.vendor.name +'</lavel><br>'\
			'				<lavel>PO No : '+ po_number +'</lavel><br>'\
			'				<lavel>PO Date : '+ str(vpo.po_date) +'</lavel><br>'\
			'				<lavel>Value : '+ str(vpo.total_value) + ' ' + str(vpo.vpo.currency) +'</lavel><br>'\
			'				<lavel>Payment Terms : '+ vpo.vpo.terms_of_payment +'</lavel><br>'\
			'			</td>		'\
			'		</tr>'\
			'	</table>'\
			'</td>	'\
		        '</tr>'
                
                try:
                        content = email_string_header + request_heading + request_details + email_string_footer
                        msg = EmailMessage(subject=po_number + ' :: Supplier Payment Request', body=content, from_email = settings.DEFAULT_FROM_EMAIL,to = ['prasannakumar.c@aeprocurex.com','sales.p@aeprocurex.com'], bcc = ['milan.kar@aeprocurex.com'])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()
                except:
                        pass
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
                        ~Q(status='Payment_Done'),
                        requester = u
                ).values(
                        'id',   
                        'vpo__po_number',
                        'vpo__po_date',
                        'vpo__vpo__vendor__name',
                        'vpo__vpo__vendor__location',
                        'amount',
                        'status'
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
                payment_request.status = 'Requested'
                payment_request.save()

                try:
                        myfile = request.FILES['supporting_document']
                        payment_request.attachment1 = myfile
                        payment_request.save()
                
                except:
                        pass

                request_heading = '<tr>'\
		        '<td class="bg_white">'\
		        '<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">'\
		        '<tr>'\
		        '<td class="bg_light email-section" style="width: 100%;">'\
		        '<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
		        '<tr>'\
			'<div class="heading-section">'\
			'<h2>Supplier Payment Request Edited</h2>'\
			'<p>A Supplier Payment Request bas Been edited By '+ u.first_name + ' ' + u.last_name +', Waiting for your approval</p>'\
			'<p><a href="'+ host_name + 'supplier_payment/payment_request/pending_approval_list_1/'+ str(request_id) +'/details/" class="btn btn-primary">Approve Now</a></p>'\
			'</div>	'\
                        '</tr>'\
                        '</table>'\
                      	'</td>'\
                        '</tr>'\
		        '</table>'\
		        '</td>'\
		        '</tr>'
                
                request_details = '<tr>'\
			'<td valign="top" class="bg_white" style="padding: 1em 2.5em;">'\
			'	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
			'		<tr>'\
			'			<td width="40%" class="logo" style="text-align: left;">'\
			'				<lavel>Supplier : '+ payment_request.vpo.vpo.vendor.name +'</lavel><br>'\
			'				<lavel>PO No : '+ payment_request.vpo.po_number +'</lavel><br>'\
			'				<lavel>PO Date : '+ str(payment_request.vpo.po_date) +'</lavel><br>'\
			'				<lavel>Value : '+ str(payment_request.vpo.total_value) + ' ' + str(payment_request.vpo.vpo.currency) +'</lavel><br>'\
			'				<lavel>Payment Terms : '+ payment_request.vpo.vpo.terms_of_payment +'</lavel><br>'\
			'			</td>		'\
			'		</tr>'\
			'	</table>'\
			'</td>	'\
		        '</tr>'
                
                try:
                        content = email_string_header + request_heading + request_details + email_string_footer
                        msg = EmailMessage(subject=payment_request.vpo.po_number + ' :: Supplier Payment Request', body=content, from_email = settings.DEFAULT_FROM_EMAIL,to = ['sales.p@aeprocurex.com'], bcc = ['milan.kar@aeprocurex.com'])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()
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
                data = request.POST
                request_details = SupplierPaymentRequest.objects.get(id=request_id)
                request_details.status = 'Rejected1'
                request_details.save()
                requester_email = request_details.vpo.requester.email
                
                po_number = request_details.vpo.po_number
                request_heading = '<tr>'\
		        '<td class="bg_white">'\
		        '<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">'\
		        '<tr>'\
		        '<td class="bg_light email-section" style="width: 100%;">'\
		        '<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
		        '<tr>'\
			'<div class="heading-section">'\
			'<h2>Payment Request Rejected</h2>'\
			'<p>A Supplier Payment Request bas Been Have Been Rejected By '+ u.first_name + ' ' + u.last_name +', Either Delete or edit this request</p>'\
			'<h3>Rejection Reason : ' + data['rejection'] + '</h3>'\
                        '</div>	'\
                        '</tr>'\
                        '</table>'\
                      	'</td>'\
                        '</tr>'\
		        '</table>'\
		        '</td>'\
		        '</tr>'
                
                request_details = '<tr>'\
			'<td valign="top" class="bg_white" style="padding: 1em 2.5em;">'\
			'	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
			'		<tr>'\
			'			<td width="40%" class="logo" style="text-align: left;">'\
			'				<lavel>Supplier : '+ request_details.vpo.vpo.vendor.name +'</lavel><br>'\
			'				<lavel>PO No : '+ request_details.vpo.po_number +'</lavel><br>'\
			'				<lavel>PO Date : '+ str(request_details.vpo.po_date) +'</lavel><br>'\
			'				<lavel>Value : '+ str(request_details.vpo.total_value) + ' ' + str(request_details.vpo.vpo.currency) +'</lavel><br>'\
			'				<lavel>Payment Terms : '+ request_details.vpo.vpo.terms_of_payment +'</lavel><br>'\
			'			</td>		'\
			'		</tr>'\
			'	</table>'\
			'</td>	'\
		        '</tr>'
                
                
                try:
                        content = email_string_header + request_heading + request_details + email_string_footer
                        msg = EmailMessage(subject= po_number + ' :: Supplier Payment Request', body=content, from_email = settings.DEFAULT_FROM_EMAIL,to = [requester_email], bcc = ['milan.kar@aeprocurex.com'])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()
                except:
                        pass

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
                po_number = request_details.vpo.po_number
                requester_email = request_details.vpo.requester.email

                request_heading = '<tr>'\
		        '<td class="bg_white">'\
		        '<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">'\
		        '<tr>'\
		        '<td class="bg_light email-section" style="width: 100%;">'\
		        '<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
		        '<tr>'\
			'<div class="heading-section">'\
			'<h2>Payment Request Approved</h2>'\
			'<p>A Supplier Payment Request bas Been Have Been Approved By '+ u.first_name + ' ' + u.last_name +', Required 2nd Approval</p>'\
			'</div>	'\
                        '</tr>'\
                        '</table>'\
                      	'</td>'\
                        '</tr>'\
		        '</table>'\
		        '</td>'\
		        '</tr>'
                
                request_details = '<tr>'\
			'<td valign="top" class="bg_white" style="padding: 1em 2.5em;">'\
			'	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
			'		<tr>'\
			'			<td width="40%" class="logo" style="text-align: left;">'\
			'				<lavel>Supplier : '+ request_details.vpo.vpo.vendor.name +'</lavel><br>'\
			'				<lavel>PO No : '+ request_details.vpo.po_number +'</lavel><br>'\
			'				<lavel>PO Date : '+ str(request_details.vpo.po_date) +'</lavel><br>'\
			'				<lavel>Value : '+ str(request_details.vpo.total_value) + ' ' + str(request_details.vpo.vpo.currency) +'</lavel><br>'\
			'				<lavel>Payment Terms : '+ request_details.vpo.vpo.terms_of_payment +'</lavel><br>'\
			'			</td>		'\
			'		</tr>'\
			'	</table>'\
			'</td>	'\
		        '</tr>'
                
                
                try:
                        content = email_string_header + request_heading + request_details + email_string_footer
                        msg = EmailMessage(subject= po_number + ' :: Supplier Payment Request', body=content, from_email = settings.DEFAULT_FROM_EMAIL,to = ['vr.shinde@aeprocurex.com',requester_email], bcc = ['milan.kar@aeprocurex.com'])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()
                except:
                        pass

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

#Lavel2 Reject 
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
                data = request.POST
                request_details = SupplierPaymentRequest.objects.get(id=request_id)
                request_details.status = 'Rejected2'
                request_details.save()
                requester_email = request_details.vpo.requester.email

                po_number = request_details.vpo.po_number
                request_heading = '<tr>'\
		        '<td class="bg_white">'\
		        '<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">'\
		        '<tr>'\
		        '<td class="bg_light email-section" style="width: 100%;">'\
		        '<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
		        '<tr>'\
			'<div class="heading-section">'\
			'<h2>Payment Request Rejected</h2>'\
			'<p>A Supplier Payment Request bas Been Have Been Rejected By '+ u.first_name + ' ' + u.last_name +', Either Delete or edit this request</p>'\
			'<h3>Rejection Reason : ' + data['rejection'] + '</h3>'\
                        '</div>	'\
                        '</tr>'\
                        '</table>'\
                      	'</td>'\
                        '</tr>'\
		        '</table>'\
		        '</td>'\
		        '</tr>'
                
                request_details = '<tr>'\
			'<td valign="top" class="bg_white" style="padding: 1em 2.5em;">'\
			'	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
			'		<tr>'\
			'			<td width="40%" class="logo" style="text-align: left;">'\
			'				<lavel>Supplier : '+ request_details.vpo.vpo.vendor.name +'</lavel><br>'\
			'				<lavel>PO No : '+ request_details.vpo.po_number +'</lavel><br>'\
			'				<lavel>PO Date : '+ str(request_details.vpo.po_date) +'</lavel><br>'\
			'				<lavel>Value : '+ str(request_details.vpo.total_value) + ' ' + str(request_details.vpo.vpo.currency) +'</lavel><br>'\
			'				<lavel>Payment Terms : '+ request_details.vpo.vpo.terms_of_payment +'</lavel><br>'\
			'			</td>		'\
			'		</tr>'\
			'	</table>'\
			'</td>	'\
		        '</tr>'
                
                
                try:
                        content = email_string_header + request_heading + request_details + email_string_footer
                        msg = EmailMessage(subject= po_number + ' :: Supplier Payment Request', body=content, from_email = settings.DEFAULT_FROM_EMAIL,to = [requester_email], bcc = ['milan.kar@aeprocurex.com'])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()
                except:
                        pass

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
                        try:
                                SupplierPaymentInfo.objects.create(
                                        payment_request = request_details,
                                        amount = data['amount'],
                                        payment_by = u,
                                        transaction_number = data['transaction_no'],
                                        transaction_date = data['transaction_date'],
                                        attachment1 = myfile
                                )
                        except:
                                SupplierPaymentInfo.objects.create(
                                        payment_request = request_details,
                                        amount = data['amount'],
                                        payment_by = u,
                                        transaction_number = data['transaction_no'],
                                        attachment1 = myfile
                                )

                        request_details.status = 'Payment_Done'
                        request_details.save()
                except:
                        try:
                                SupplierPaymentInfo.objects.create(
                                        payment_request = request_details,
                                        amount = data['amount'],
                                        transaction_number = data['transaction_no'],
                                        transaction_date = data['transaction_date'],
                                        payment_by = u
                                )
                        except:
                                SupplierPaymentInfo.objects.create(
                                        payment_request = request_details,
                                        amount = data['amount'],
                                        transaction_number = data['transaction_no'],
                                        payment_by = u
                                )


                        request_details.status = 'Payment_Done'
                        request_details.save()
                
                po_number = request_details.vpo.po_number
                request_heading = '<tr>'\
		        '<td class="bg_white">'\
		        '<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">'\
		        '<tr>'\
		        '<td class="bg_light email-section" style="width: 100%;">'\
		        '<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
		        '<tr>'\
			'<div class="heading-section">'\
			'<h2>Supplier Payment Done </h2>'\
			'<p>Final Payment Request has Been Approved By '+ u.first_name + ' ' + u.last_name +', Please check the payment information</p>'\
			'</div>	'\
                        '</tr>'\
                        '</table>'\
                      	'</td>'\
                        '</tr>'\
		        '</table>'\
		        '</td>'\
		        '</tr>'
                
                request_details = '<tr>'\
			'<td valign="top" class="bg_white" style="padding: 1em 2.5em;">'\
			'	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
			'		<tr>'\
			'			<td width="40%" class="logo" style="text-align: left;">'\
			'				<lavel>Supplier : '+ request_details.vpo.vpo.vendor.name +'</lavel><br>'\
			'				<lavel>PO No : '+ request_details.vpo.po_number +'</lavel><br>'\
			'				<lavel>PO Date : '+ str(request_details.vpo.po_date) +'</lavel><br>'\
			'				<lavel>Value : '+ str(request_details.vpo.total_value) + ' ' + str(request_details.vpo.vpo.currency) +'</lavel><br>'\
			'				<lavel>Payment Terms : '+ request_details.vpo.vpo.terms_of_payment +'</lavel><br>'\
			'			</td>		'\
			'		</tr>'\
			'	</table>'\
			'</td>	'\
		        '</tr>'
                
                
                try:
                        content = email_string_header + request_heading + request_details + email_string_footer
                        msg = EmailMessage(subject= po_number + ' :: Supplier Payment Request', body=content, from_email = settings.DEFAULT_FROM_EMAIL,to = ['milan.kar@aeprocurex.com'], bcc = [''])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()
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

#All Supplier Payment List
@login_required(login_url="/employee/login/")
def SupplierPaymentWave(request, id = None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                request_details = SupplierPaymentRequest.objects.get(id=id)
                context['request_details'] = request_details

                vpo_lineitem = VendorPOLineitems.objects.filter(vpo=request_details.vpo.vpo)
                context['vpo'] = request_details.vpo
                context['vpo_lineitem'] = vpo_lineitem

                if type == 'Sourcing':
                        return render(request,"Sourcing/SupplierPayment/payment_request_wave.html",context)

        if request.method == 'POST':
                request_details = SupplierPaymentRequest.objects.get(id=id)
                po_number = request_details.vpo.po_number
                request_heading = '<tr>'\
		        '<td class="bg_white">'\
		        '<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">'\
		        '<tr>'\
		        '<td class="bg_light email-section" style="width: 100%;">'\
		        '<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
		        '<tr>'\
			'<div class="heading-section">'\
			'<h2>Supplier Payment - Wave</h2>'\
			'<p> ' + u.first_name + ' ' + u.last_name +' is waiving at for making the supplier payment</p>'\
			'</div>	'\
                        '</tr>'\
                        '</table>'\
                      	'</td>'\
                        '</tr>'\
		        '</table>'\
		        '</td>'\
		        '</tr>'
                
                request_details = '<tr>'\
			'<td valign="top" class="bg_white" style="padding: 1em 2.5em;">'\
			'	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">'\
			'		<tr>'\
			'			<td width="40%" class="logo" style="text-align: left;">'\
			'				<lavel>Supplier : '+ request_details.vpo.vpo.vendor.name +'</lavel><br>'\
			'				<lavel>PO No : '+ request_details.vpo.po_number +'</lavel><br>'\
			'				<lavel>PO Date : '+ str(request_details.vpo.po_date) +'</lavel><br>'\
			'				<lavel>Value : '+ str(request_details.vpo.total_value) + ' ' + str(request_details.vpo.vpo.currency) +'</lavel><br>'\
			'				<lavel>Payment Terms : '+ request_details.vpo.vpo.terms_of_payment +'</lavel><br>'\
			'			</td>		'\
			'		</tr>'\
			'	</table>'\
			'</td>	'\
		        '</tr>'
                
                #try:
                content = email_string_header + request_heading + request_details + email_string_footer
                msg = EmailMessage(subject=po_number + ' :: Supplier Payment Request', body=content, from_email = settings.DEFAULT_FROM_EMAIL,to = ['prasannakumar.c@aeprocurex.com','sales.p@aeprocurex.com'], bcc = ['milan.kar@aeprocurex.com'])
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                #except:
                #        pass

                return HttpResponseRedirect(reverse('supplier-payment-applied-list'))

#Accounts Supplier Payment List
@login_required(login_url="/employee/login/")
def AccountsSupplierPaymentList(request):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name               

        if request.method == 'GET':
                if type == 'Accounts':
                        payment_info = SupplierPaymentInfo.objects.filter(acknowledgement = 'no').values(
                                'id',
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
                        return render(request,"Accounts/SupplierPayment/supplier_payment_all_list.html",context)
                        
#Accounts Supplier Payment List
@login_required(login_url="/employee/login/")
def AccountsPaymentDetails(request, id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                payment = SupplierPaymentInfo.objects.get(id = id)
                request_id = payment.payment_request.id
                request_details = SupplierPaymentRequest.objects.get(id=request_id)
                context['request_details'] = request_details

                context['payment'] = payment
                vpo_lineitem = VendorPOLineitems.objects.filter(vpo=request_details.vpo.vpo)
                context['vpo'] = request_details.vpo
                context['vpo_lineitem'] = vpo_lineitem

                if type == 'Accounts':
                        return render(request,"Accounts/SupplierPayment/payment_details.html",context)                

#Accounts add payment info
@login_required(login_url="/employee/login/")
def AccountsPaymentDetailsAddInfo(request, id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                payment = SupplierPaymentInfo.objects.get(id = id)
                context['payment'] = payment

                if type == 'Accounts':
                        return render(request,"Accounts/SupplierPayment/add_payment_info.html",context)

        if request.method == 'POST':
                data = request.POST
                payment = SupplierPaymentInfo.objects.get(id = id)

                print(data['transaction_no'])
                print(data['transaction_date'])

                try:
                        myfile = request.FILES['supporting_document']
                        try:
                                payment.transaction_number = data['transaction_no']

                                if str(data['transaction_date']) != '':
                                        payment.transaction_date = data['transaction_date']
                                
                                payment.attachment1 = myfile
                                #payment.save()

                        except:
                                payment.transaction_number = data['transaction_no']
                                payment.attachment1 = myfile   
                                #payment.save() 

                except:
                        try:
                                payment.transaction_number = data['transaction_no']

                                if str(data['transaction_date']) != '':
                                        payment.transaction_date = data['transaction_date']

                                #payment.save()

                        except:
                                payment.transaction_number = data['transaction_no']
                                #payment.save()
                payment.save()
                return HttpResponseRedirect(reverse('accounts-payment-details',args=[id]))

#Accounts payment Mark acknowledge
@login_required(login_url="/employee/login/")
def AccountsPaymentDetailsAcknowledge(request, id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'POST':
                data = request.POST
                payment = SupplierPaymentInfo.objects.get(id = id)

                payment.acknowledgement = 'yes'
                payment.save()                
                return HttpResponseRedirect(reverse('accounts-supplier-payment-list'))  

#Accounts Supplier Payment  Acknowledge List
@login_required(login_url="/employee/login/")
def AccountsPaymentAcknowledgeList(request):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name               

        if request.method == 'GET':
                if type == 'Accounts':
                        payment_info = SupplierPaymentInfo.objects.filter(acknowledgement = 'yes').values(
                                'id',
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
                        return render(request,"Accounts/SupplierPayment/acknowledge_supplier_payment_list.html",context)

#Accounts Supplier Payment Acknowledge details
@login_required(login_url="/employee/login/")
def AccountsPaymentAcknowledgeDetails(request, id=None):
        context={}
        context['supplier_payment'] = 'active'
        u = User.objects.get(username=request.user)
        type = u.profile.type
        context['login_user_name'] = u.first_name + ' ' + u.last_name

        if request.method == 'GET':
                payment = SupplierPaymentInfo.objects.get(id = id)
                request_id = payment.payment_request.id
                request_details = SupplierPaymentRequest.objects.get(id=request_id)
                context['request_details'] = request_details

                context['payment'] = payment
                vpo_lineitem = VendorPOLineitems.objects.filter(vpo=request_details.vpo.vpo)
                context['vpo'] = request_details.vpo
                context['vpo_lineitem'] = vpo_lineitem

                if type == 'Accounts':
                        return render(request,"Accounts/SupplierPayment/payment_acknowledge-details.html",context)                

