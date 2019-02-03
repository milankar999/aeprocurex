from django.db import models
from Customer.models import *
from Quotation.models import *
import uuid

class CPOCreationDetail(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        creation_date = models.DateTimeField(auto_now_add=True)
        created_by = models.ForeignKey(User,on_delete = models.CASCADE)

        def __str__(self):
                return  self.created_by.username + '    ' + str(self.creation_date)

class CPOApprovalDetail(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        approved_date = models.DateTimeField(auto_now_add=True)
        approved_by = models.ForeignKey(User,on_delete = models.CASCADE)

        def __str__(self):
                return str(self.approved_date) + '     ' + self.approved_by.username

class CPOAssign(models.Model):
        id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
        assign_to = models.ForeignKey(User,on_delete = models.CASCADE)
    
        def __str__(self):
                return self.assign_to.username

class CustomerPO(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
        customer_contact_person = models.ForeignKey(CustomerContactPerson,on_delete=models.CASCADE)
        delivery_contact_person = models.ForeignKey(DeliveryContactPerson,null=True,blank=True,on_delete=models.CASCADE)

        customer_po_no = models.CharField(max_length=200)
        customer_po_date = models.DateField()
        delivery_date = models.DateField()
        billing_address = models.TextField()
        shipping_address = models.TextField()
        inco_terms = models.CharField(max_length = 200)
        payment_terms = models.IntegerField(default = 0)
        status = models.CharField(max_length = 100, default='creation_inprogress')

        cpo_creation_detail = models.ForeignKey(CPOCreationDetail,on_delete = models.CASCADE,null=True, blank=True)
        cpo_approval_detail = models.ForeignKey(CPOApprovalDetail,on_delete = models.CASCADE,null=True, blank=True)
        cpo_assign_detail = models.ForeignKey(CPOAssign, on_delete = models.CASCADE,null=True, blank=True)

        def __str__(self):
                return self.customer_po_no + ' ' + self.customer.name + ' ' + self.cpo_assign_detail.creation_date

class CPOLineitem(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        cpo = models.ForeignKey(CustomerPO,on_delete=models.CASCADE)
        quotation_lineitem = models.ForeignKey(QuotationLineitem,on_delete=models.CASCADE, null=True, blank=True)
        product_title = models.CharField(max_length=200,null = False, blank = False)
        description = models.TextField(null=False, blank=False)
        model = models.CharField(max_length=200,null = True, blank = True)
        brand = models.CharField(max_length=200,null = True, blank = True)
        product_code = models.CharField(max_length=200,null = True, blank = True)
        part_no = models.CharField(max_length=200,null = True, blank = True)
        category = models.CharField(max_length=200,null = True, blank = True)
        hsn_code = models.CharField(max_length=10,null = True, blank = True)
        gst = models.FloatField(null = True, blank = True)
        uom = models.CharField(max_length=20,null = False, blank = False, default='Pcs')
        quantity = models.FloatField(null = False, blank = False)
        unit_price = models.FloatField(null = False, blank = False)

        def __str__(self):
                return self.product_title + ' ' + self.quantity + ' ' + self.unit_price