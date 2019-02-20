from django.contrib import admin
from .models import *

admin.site.register(CPOCreationDetail)
admin.site.register(CPOApprovalDetail)
admin.site.register(CPOAssign)
admin.site.register(CustomerPO)
admin.site.register(CPOLineitem)
admin.site.register(CPOSelectedQuotation)