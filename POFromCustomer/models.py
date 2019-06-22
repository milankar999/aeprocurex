from django.db import models
from Customer.models import *
from Quotation.models import *
import uuid

class CPOCreationDetail(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        creation_date = models.DateTimeField(auto_now_add=True)
        created_by = models.ForeignKey(User,on_delete = models.SET_NULL,null=True,blank=True)

        def __str__(self):
                return  self.created_by.username + '    ' + str(self.creation_date)

class CPOApprovalDetail(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        approved_date = models.DateTimeField(auto_now_add=True)
        approved_by = models.ForeignKey(User,on_delete = models.SET_NULL,null=True,blank=True)

        def __str__(self):
                return str(self.approved_date) + '     ' + self.approved_by.username

class CPOAssign(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        assign_to = models.ForeignKey(User,on_delete = models.SET_NULL,null=True,blank=True)
        
        assigned_time = models.DateTimeField(auto_now_add=True)
        def __str__(self):
                return self.assign_to.username 

class CustomerPO(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
        customer_contact_person = models.ForeignKey(CustomerContactPerson,on_delete=models.SET_NULL,null=True,blank=True)
        delivery_contact_person = models.ForeignKey(DeliveryContactPerson,null=True,blank=True,on_delete=models.SET_NULL)

        customer_po_no = models.CharField(max_length=200,null=True,blank=True)
        customer_po_date = models.DateField(null=True,blank=True)
        delivery_date = models.DateField(null=True,blank=True)
        billing_address = models.TextField(null=True,blank=True)
        shipping_address = models.TextField(null=True,blank=True)
        inco_terms = models.CharField(max_length = 200,null=True,blank=True)
        payment_terms = models.IntegerField(default = 0,null=True,blank=True)
        status = models.CharField(max_length = 100, default='creation_inprogress')
        po_type = models.CharField(max_length = 100, null=True, blank=True) 

        rejection_reason = models.TextField(null=True, blank = True)

        cpo_creation_detail = models.ForeignKey(CPOCreationDetail,on_delete = models.CASCADE,null=True, blank=True)
        cpo_approval_detail = models.ForeignKey(CPOApprovalDetail,on_delete = models.CASCADE,null=True, blank=True)
        cpo_assign_detail = models.ForeignKey(CPOAssign, on_delete = models.CASCADE,null=True, blank=True)

        segmentation = models.BooleanField(default=False)

        total_basic_value = models.FloatField(null = False, blank = False, default = 0)
        total_value = models.FloatField(null = False, blank = False, default = 0)
        
        document1 = models.FileField(upload_to='cpo/',null=True,blank=True)
        document2 = models.FileField(upload_to='cpo/',null=True,blank=True)

        lineitem_copy_status = models.BooleanField(default=False)

        def __str__(self):
                return str(self.customer_po_no) + ' ' + str(self.customer.name)

class CPOSelectedQuotation(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        quotation = models.ForeignKey(QuotationTracker,on_delete=models.SET_NULL,null=True,blank=True)
        customer_po = models.ForeignKey(CustomerPO,on_delete=models.CASCADE)

        def __str__(self):
                return self.quotation.quotation_no + ' ' + self.customer_po.customer.name
        
class CPOLineitem(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        cpo = models.ForeignKey(CustomerPO,on_delete=models.CASCADE)
        quotation_lineitem = models.ForeignKey(QuotationLineitem,on_delete=models.SET_NULL, null=True, blank=True)
        product_title = models.CharField(max_length=200,null = False, blank = False)
        description = models.TextField(null=False, blank=False)
        model = models.CharField(max_length=200,null = True, blank = True)
        brand = models.CharField(max_length=200,null = True, blank = True)
        product_code = models.CharField(max_length=200,null = True, blank = True)
        part_no = models.CharField(max_length=200,null = True, blank = True)
        hsn_code = models.CharField(max_length=10,null = True, blank = True)
        pack_size = models.CharField(max_length=10,null = True, blank = True)
        gst = models.FloatField(null = True, blank = True, default = 0)
        uom = models.CharField(max_length=20,null = False, blank = False, default='Pcs')
        quantity = models.FloatField(null = False, blank = False)
        unit_price = models.FloatField(null = False, blank = False)
        total_basic_price = models.FloatField(null = False, blank = False, default = 0)
        total_price = models.FloatField(null = False, blank = False, default = 0)

        segment_status = models.BooleanField(default=False)

        pending_po_releasing_quantity = models.FloatField(null=True, blank=True, default=0)
        direct_receivable_quantity = models.FloatField(null=True, blank=True, default=0)

        pending_delivery_quantity = models.FloatField(null=True, blank=True, default=0)

        def __str__(self):
                return self.product_title + ' ' + str(self.quantity) + ' ' + str(self.unit_price)
