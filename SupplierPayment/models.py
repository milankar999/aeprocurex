from django.db import models
from POForVendor.models import *
from BankAccount.models import *
import uuid

class SupplierPaymentRequest(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        vpo = models.ForeignKey(VendorPOTracker, on_delete=models.CASCADE)

        amount = models.FloatField(default=0)
        notes = models.TextField(null=True, blank=True)

        status = models.CharField(max_length=20, default='Requested')
        requester = models.ForeignKey(User, on_delete=models.CASCADE)
        date = models.DateTimeField(auto_now_add=True)

        attachment1 = models.FileField(upload_to='supplier_payment_request/',null=True,blank=True)
        #attachment2 = models.FileField(upload_to='supplier_payment_request/',null=True,blank=True)
        #attachment3 = models.FileField(upload_to='supplier_payment_request/',null=True,blank=True)

        def __str__(self):
                return str(self.vpo.po_number) + ' / ' + str(self.amount)


class SupplierPaymentInfo(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        payment_request = models.ForeignKey(SupplierPaymentRequest, on_delete=models.CASCADE)
        
        amount = models.FloatField(default=0)
        payment_by = models.ForeignKey(User, on_delete=models.CASCADE)

        attachment1 = models.FileField(upload_to='supplier_payment/',null=True,blank=True)
        #attachment2 = models.FileField(upload_to='supplier_payment/',null=True,blank=True)
        #attachment3 = models.FileField(upload_to='supplier_payment/',null=True,blank=True)
        transaction_number = models.CharField(max_length = 200, null=True, blank=True)
        transaction_date = models.DateField(null=True, blank=True)

        payment_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
        bank = models.ForeignKey(VendorBankAccount, on_delete = models.SET_NULL, null=True, blank = True)

        acknowledgement = models.CharField(max_length = 200, default = 'no')

        def __str__(self):
                return str(self.payment_request.vpo.po_number) + ' / ' + str(self.amount)

