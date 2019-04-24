from django.contrib import admin
from .views import *

admin.site.register(CurrencyIndex)
admin.site.register(VendorPO)
admin.site.register(VendorPOTracker)
admin.site.register(VendorPOLineitems)
admin.site.register(VPOStatus)