from django.db import models
from django.contrib.auth.models import User
from Customer.models import *
from RFP.models import *
from Sourcing.models import *
import uuid

class QuotationTracker(models.Model):
    quotation_no = models.CharField(max_length=100,null=False,blank=False,primary_key=True)
    rfp = models.ForeignKey(RFP,on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    customer_contact_person = models.ForeignKey(CustomerContactPerson,on_delete=models.CASCADE)
    
    status = models.CharField(max_length=200,null=True,blank=True,default='processing')

    enquiry_reference = models.CharField(max_length=200,null=True,blank=True)

    price_validity = models.CharField(max_length=200,null=True,blank=True,default='30 Days')
    quotation_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete = models.CASCADE)
    comments = models.TextField(null=True,blank=True)

    tc1 = models.TextField(null=True,blank=True)
    tc2 = models.TextField(null=True,blank=True)
    tc3 = models.TextField(null=True,blank=True)
    tc4 = models.TextField(null=True,blank=True)
    tc5 = models.TextField(null=True,blank=True)
    tc6 = models.TextField(null=True,blank=True)
    tc7 = models.TextField(null=True,blank=True)
    tc8 = models.TextField(null=True,blank=True)
    tc9 = models.TextField(null=True,blank=True)
    tc10 = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.quotation_no + ',' + str(self.quotation_date) + ',' + self.customer.name

class QuotationLineitem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quotation = models.ForeignKey(QuotationTracker,on_delete=models.CASCADE)
    sourcing_lineitem = models.ForeignKey(SourcingLineitem, on_delete = models.CASCADE, null=True, blank=True)

    product_title = models.CharField(max_length=200,null = False, blank = False)
    description = models.TextField(null=False, blank=False)
    model = models.CharField(max_length=200,null = True, blank = True)
    brand = models.CharField(max_length=200,null = True, blank = True)
    product_code = models.CharField(max_length=200,null = True, blank = True)
    part_number = models.CharField(max_length=200, null=True, blank=True)

    pack_size = models.CharField(max_length=200,null = True, blank = True)
    moq = models.CharField(max_length=200,null = True, blank = True)

    hsn_code = models.CharField(max_length=200, null=True, blank=True)
    gst = models.FloatField(null = True, blank = True)
    
    quantity = models.FloatField(null = False, blank = False)
    uom = models.CharField(max_length=20,null = False, blank = False)

    unit_price = models.FloatField(null = True, blank = True)
    margin = models.FloatField(null=True, blank=True)

    lead_time = models.CharField(max_length=200,null = True, blank = True)

    def __str__(self):
        return self.product_title