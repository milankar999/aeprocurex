from django.db import models
from POFromCustomer.models import *
from Customer.models import *
import uuid

class PendingDelivery(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        cpo_lineitem = models.ForeignKey(CPOLineitem,on_delete = models.CASCADE)

        pending_quantity = models.FloatField(null=True,blank=True)

        def __str__(self):
                return self.cpo_lineitem.product_title + ' ' + str(self.pending_quantity)

class InvoiceTracker(models.Model):
        invoice_no = models.CharField(max_length = 20, primary_key=True)
        invoice_date = models.DateField(auto_now_add = True,null=True, blank=True)
        cpo = models.ForeignKey(CustomerPO,on_delete = models.CASCADE, null=True, blank=True)

        customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
        customer_contact_person = models.ForeignKey(CustomerContactPerson,on_delete = models.CASCADE, null=True, blank=True)

        billing_address = models.TextField(null=True, blank=True)
        shipping_address = models.TextField(null=True, blank=True)

        po_reference = models.CharField(max_length = 200, null=True, blank=True)
        po_date = models.DateField(null=True, blank=True)

        basic_value = models.FloatField(default = 0)
        total_value = models.FloatField(default = 0)

        generating_status = models.CharField(max_length = 200, default='creation_in_progress')
        financial_year = models.CharField(max_length = 20, null = True, blank = True)        

        def __str__(self):
                return self.invoice_no + ' ' + self.customer.name + ' ' + str(self.total_value)

class InvoiceLineitem(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        invoice = models.ForeignKey(InvoiceTracker, on_delete = models.CASCADE)

        product_title = models.CharField(max_length = 200)
        description = models.TextField()
        model = models.CharField(max_length = 200, null=True, blank = True)
        brand = models.CharField(max_length = 200, null=True, blank = True)
        product_code = models.CharField(max_length = 200, null=True, blank = True)
        part_number = models.CharField(max_length = 200, null=True, blank = True)
        hsn_code = models.CharField(max_length=20, null=True, blank = True)

        quantity = models.FloatField(default=1)
        uom = models.CharField(max_length = 20, default = 'PC')

        unit_price = models.FloatField(default = 0)

        total_basic_price = models.FloatField(default = 0)
        gst = models.FloatField(default = 0)
        total_price = models.FloatField(default = 0)

        

        def __str__(self):
                return self.invoice.invoice_no + ' ' + self.product_title + ' ' + str(self.quantity)

