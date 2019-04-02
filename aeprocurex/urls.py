"""aeprocurex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Employee.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Employee.urls')),
    path('employee/',include('Employee.urls')),
    path('api/employee/',include('Employee.api_urls')),
    path('customer/',include('Customer.urls')),
    path('supplier/',include('Supplier.urls')),
    path('rfp/',include('RFP.urls')),
    path('sourcing/',include('Sourcing.urls')),
    path('key_accounts/',include('KeyAccounts.urls')),
    path('COQ/',include('COQ.urls')),
    path('quotation/',include('Quotation.urls')),

    #PO FROM CUSTOMER
    path('po_from_customer/',include('POFromCustomer.urls')),
    path('api/po_from_customer/',include('POFromCustomer.api_urls')),

    path('invoice/',include('Invoice.urls')),
    path('grnir/',include('GRNIR.urls')),

    path('api/po_8_vendor/',include('POToVendor.urls')),
    path('api/po_to_vendor/',include('POForVendor.urls')),
    path('api/leaves/',include('Leaves.urls')),
    path('api/expences/',include('Expences.api_urls')),
    path('expences/',include('Expences.urls')),
    path('enquiry_tracker/',include('EnquiryTracker.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)