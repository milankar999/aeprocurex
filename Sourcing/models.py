from django.db import models
from django.contrib.auth.models import User
from Supplier.models import *
from RFP.models import *
import uuid

class Sourcing(models.Model):
    id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
    rfp =  models.ForeignKey(RFP,on_delete = models.CASCADE)
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE)
    supplier_contact_person = models.ForeignKey(SupplierContactPerson, on_delete = models.CASCADE)
    offer_reference = models.CharField(max_length=200)
    offer_date = models.DateField()

    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return  self.rfp.rfp_no + '    ' + str(self.creation_date) + '  ' + self.offer_reference

class SourcingLineitem(models.Model):
    id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
    sourcing = models.ForeignKey(Sourcing, on_delete = models.CASCADE)
    rfp_lineitem = models.ForeignKey(RFPLineitem, on_delete = models.CASCADE)

    product_title = models.CharField(max_length=200,null = False, blank = False)
    description = models.TextField(null=False, blank=False)
    model = models.CharField(max_length=200,null = True, blank = True)
    brand = models.CharField(max_length=200,null = True, blank = True)
    product_code = models.CharField(max_length=200,null = True, blank = True)

    pack_size = models.CharField(max_length=200,null = True, blank = True)
    moq = models.CharField(max_length=200,null = True, blank = True)
    lead_time = models.CharField(max_length=200,null = True, blank = True)
    price_validity = models.CharField(max_length=200,null = True, blank = True)

    expected_freight = models.FloatField(null=True,blank=True)

    mrp = models.FloatField(null = True, blank = True)
    price1 = models.FloatField(null = True, blank = True)
    price2 = models.FloatField(null = True, blank = True)
    mark = models.CharField(max_length = 10, default='False')

    creation_time = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.product_title + ' ' + str(self.price1)

class SourcingAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sourcing = models.ForeignKey(Sourcing, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='supplier_quotation/',null=True,blank=True)
    quotation_link = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.sourcing.id

class SourcingCharges(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sourcing = models.ForeignKey(Sourcing, on_delete=models.CASCADE)
    cost_description = models.CharField(max_length=200,null=True,blank=True)

    value = models.FloatField(default = 0)

    def __str__(self):
        return self.sourcing.id

class RFQ(models.Model):
    id = models.CharField(max_length=200,primary_key=True)
    sourcing = models.ForeignKey(Sourcing, on_delete = models.CASCADE)

    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.id

class RFQLineitem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfq = models.ForeignKey(RFQ, on_delete= models.CASCADE)
    rfp_lineitem = models.ForeignKey(RFPLineitem, on_delete=models.CASCADE)

    def __str__(self):
        return self.id