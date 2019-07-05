from django.db import models
from POForVendor.models import *
from Supplier.models import *
from POFromCustomer.models import *
import uuid

class GRNTracker(models.Model):
        grn_no = models.CharField(max_length=50,primary_key=True)
        vpo = models.ForeignKey(VendorPOTracker,null=True,blank=True,on_delete=models.SET_NULL)
        cpo = models.ForeignKey(CustomerPO,null=True,blank=True,on_delete=models.SET_NULL)
        vendor = models.ForeignKey(SupplierProfile,on_delete=models.CASCADE)

        date = models.DateTimeField(auto_now_add=True)
        grn_by = models.ForeignKey(User,on_delete=models.CASCADE)

        financial_year = models.CharField(max_length=50,null=True,blank=True)

        status = models.CharField(max_length=50,null=True,blank=True,default = 'creation_in_progress')
        ir_status = models.CharField(max_length=50,null=True,blank=True,default = 'incomplete')

        grn_type = models.CharField(max_length=30, default='regular')

        def __str__(self):
                return self.vendor.name + ' ' + str(self.date)

class GRNLineitem(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        grn = models.ForeignKey(GRNTracker,on_delete=models.CASCADE)

        vpo_lineitem = models.ForeignKey(VendorPOLineitems,null=True,blank=True,on_delete=models.CASCADE)
        cpo_lineitem = models.ForeignKey(CPOLineitem,null=True,blank=True,on_delete=models.CASCADE)

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
        
class GRNAttachment(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

        grn = models.ForeignKey(GRNTracker,on_delete=models.CASCADE)

        description = models.CharField(max_length=100, null = True, blank = True)
        document_no = models.CharField(max_length=100, null = True, blank = True)
        document_date = models.DateField()

        attachment = models.FileField(upload_to='grn_document/')

        def __str__(self):
                return self.document_no + str(self.document_date)

class IRTracker(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

        grn = models.ForeignKey(GRNTracker,on_delete=models.CASCADE)
        invoice_no = models.CharField(max_length = 200)
        invoice_date = models.DateTimeField()

        total_basic_price = models.FloatField()
        total_price = models.FloatField()

        received_currency = models.ForeignKey(CurrencyIndex, on_delete = models.CASCADE, default=CurrencyIndex.DEFAULT_PK)
        inr_value = models.FloatField(default=1)

        converted_total_basic_price = models.FloatField()
        converted_total_price = models.FloatField()
        comments = models.TextField(null=True, blank=True)

        def __str__(self):
                return self.grn.grn_no + self.invoice_no

class IRAttachment(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

        ir= models.ForeignKey(IRTracker,on_delete=models.CASCADE)

        description = models.CharField(max_length=100, null = True, blank = True)
        document_no = models.CharField(max_length=100, null = True, blank = True)
        document_date = models.DateField()

        attachment = models.FileField(upload_to='ir_document/')

        def __str__(self):
                return self.document_no + str(self.document_date)