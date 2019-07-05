from django.db import models
from Supplier.models import *
import uuid

class BankAccountList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bank_name = models.CharField(max_length=200)
    account_holder = models.CharField(max_length=200)
    ifcs_code = models.CharField(max_length = 200)

    def __str__(self):
        return self.bank_name + ' : ' + self.account_holder + ' : ' + self.ifcs_code

class VendorBankAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(SupplierProfile, on_delete = models.SET_NULL, null=True, blank=True)
    bank_name = models.CharField(max_length=200)
    branch = models.CharField(max_length = 200, null=True, blank=True)
    account_holder = models.CharField(max_length=200)
    ifcs_code = models.CharField(max_length = 200)
    account_type = models.CharField(max_length = 200)

    def __str__(self):
        return  self.supplier.name +' - ' + self.bank_name + ' : ' + self.account_holder + ' : ' + self.ifcs_code
