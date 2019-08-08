from django.contrib import admin

from .models import *

admin.site.register(PendingDelivery)
admin.site.register(InvoiceTracker)
admin.site.register(InvoiceLineitem)
admin.site.register(InvoiceGRNLink)
