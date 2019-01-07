from django.db import models
from django.contrib.auth.models import User
from Sourcing.models import *

class COQLineitem(models.Model):
    id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
    sourcing_lineitem = models.ForeignKey(SourcingLineitem, on_delete = models.CASCADE, null=True, blank=True)

    rfp_no = models.CharField(max_length=200,null=True,blank=True)

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

    expected_freight = models.FloatField(null=True,blank=True)

    unit_price = models.FloatField(null = True, blank = True)
    margin = models.FloatField(default=15)

    lead_time = models.CharField(max_length=200,null = True, blank = True)

    def __str__(self):
        return self.product_title + ' ' + str(self.margin)