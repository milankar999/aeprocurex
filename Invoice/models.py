from django.db import models
from POFromCustomer.models import *
from POForVendor.models import *
from GRNIR.models import *
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
        
        requester = models.CharField(max_length = 200, null=True, blank=True)
        requester_phone_no = models.CharField(max_length = 200, null=True, blank=True)

        receiver = models.CharField(max_length = 200, null=True, blank=True)
        receiver_department = models.CharField(max_length = 200, null=True, blank=True)
        receiver_phone_no = models.CharField(max_length = 200, null=True, blank=True)

        po_reference = models.CharField(max_length = 200, null=True, blank=True)
        po_date = models.DateField(null=True, blank=True)

        remarks = models.TextField(null=True, blank=True)

        other_info1 = models.TextField(null=True, blank=True)
        other_info2 = models.TextField(null=True, blank=True)
        other_info3 = models.TextField(null=True, blank=True)
        other_info4 = models.TextField(null=True, blank=True)
        other_info5 = models.TextField(null=True, blank=True)
        other_info6 = models.TextField(null=True, blank=True)
        other_info7 = models.TextField(null=True, blank=True)


        basic_value = models.FloatField(default = 0)
        total_value = models.FloatField(default = 0)

        generating_status = models.CharField(max_length = 200, default='creation_in_progress')
        financial_year = models.CharField(max_length = 20, null = True, blank = True) 

        acknowledgement = models.CharField(max_length = 20, default = 'No')       

        def __str__(self):
                return self.invoice_no + ' ' + self.customer.name + ' ' + str(self.total_value)

class InvoiceLineitem(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        invoice = models.ForeignKey(InvoiceTracker, on_delete = models.CASCADE)

        customer_po_lineitem = models.ForeignKey(CPOLineitem, null=True, blank=True, on_delete = models.SET_NULL)

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

class InvoiceGRNLink(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

        invoice_lineitem = models.ForeignKey(InvoiceLineitem, null=True, blank=True, on_delete = models.CASCADE)
        grn_lineitem = models.ForeignKey(GRNLineitem, null=True, blank=True, on_delete=models.CASCADE)

        quantity = models.FloatField(default = 0.0)

        def __str__(self):
                return self.invoice_lineitem.invoice.invoice_no + ' ' + str(self.quantity)

class AcknowledgeDocument(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

        invoice = models.ForeignKey(InvoiceTracker, on_delete = models.CASCADE)
        description = models.TextField(null=True, blank = True)
        date = models.DateField()

        document = models.FileField(upload_to='invoice_ack/')

        def __str__(self):
                return self.invoice.invoice_no + ' ' + str(self.date)