from django.db import models
from POForVendor.models import *
from Supplier.models import *
import uuid

class GRNTracker(models.Model):
        grn_no = models.CharField(max_length=50,primary_key=True)
        vpo = models.ForeignKey(VendorPOTracker,null=True,blank=True,on_delete=models.CASCADE)
        vendor = models.ForeignKey(SupplierProfile,on_delete=models.CASCADE)

        date = models.DateTimeField(auto_now_add=True)
        grn_by = models.ForeignKey(User,on_delete=models.CASCADE)

        financial_year = models.CharField(max_length=50,null=True,blank=True)

        status = models.CharField(max_length=50,null=True,blank=True,default = 'creation_in_progress')

        def __str__(self):
                return self.vendor.name + ' ' + str(self.date)

class GRNLineitem(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        grn = models.ForeignKey(GRNTracker,on_delete=models.CASCADE)

        vpo_lineitem = models.ForeignKey(VendorPOLineitems,null=True,blank=True,on_delete=models.CASCADE)

        product_title = models.CharField(max_length=200,null = False, blank = False)
        description = models.TextField(null=False, blank=False)
        model = models.CharField(max_length=200,null = True, blank = True)
        brand = models.CharField(max_length=200,null = True, blank = True)
        product_code = models.CharField(max_length=200,null = True, blank = True)
        
        hsn_code = models.CharField(max_length=10,null = True, blank = True)
        pack_size = models.CharField(max_length=10,null = True, blank = True)
        
        uom = models.CharField(max_length=20,null = False, blank = False, default='Pcs')
        quantity = models.FloatField(null = False, blank = False)
        unit_price = models.FloatField(null = False, blank = False,default = 0)
        gst = models.FloatField(null = True, blank = True, default=0)

        total_basic_price = models.FloatField(default=0)
        total_price = models.FloatField(default=0)

        def __str__(self):
                return self.grn.grn_no + self.product_title
        

        