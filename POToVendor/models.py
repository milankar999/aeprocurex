from django.db import models
from POFromCustomer.models import *
from Supplier.models import *
import uuid

class VPORequester(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        requester = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

        def __str__(self):
                return self.requester.username

class VPOReceiver(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        receiver = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

        def __str__(self):
                return self.requester

class VPO(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        cpo = models.ForeignKey(CustomerPO,on_delete=models.CASCADE)
        vendor = models.ForeignKey(SupplierProfile,on_delete=models.CASCADE)
        vendor_contact_person = models.ForeignKey(SupplierContactPerson,on_delete=models.CASCADE)

        offer_reference =  models.CharField(max_length=100,null=True,blank=True)
        offer_date = models.DateField(null=True,blank=True)

        billing_address = models.TextField(null=True,blank=True)
        shipping_address = models.TextField(null=True,blank=True)
        delivery_date = models.DateField(null=True, blank=True)

        po_number = models.CharField(max_length=100,null=True,blank=True)
        po_date = models.DateField(null=True,blank=True)

        requester = models.ForeignKey(VPORequester,on_delete=models.CASCADE,null=True,blank=True)
        receiver = models.ForeignKey(VPOReceiver,on_delete=models.CASCADE,null=True,blank=True)

        payment_term = models.IntegerField(default=0)
        advance_percentage = models.IntegerField(default=0)

        freight_charges = models.FloatField(default = 0.0)
        custom_duties = models.FloatField(default = 0.0)
        pf = models.FloatField(default = 0.0)
        insurance = models.FloatField(default = 0.0)
        
        mode_of_transport = models.CharField(max_length=200,null=True,blank=True)
        inco_terms = models.CharField(max_length=200,null=True,blank=True)
        installation = models.CharField(max_length=200,null=True,blank=True)

        currency = models.CharField(max_length=20,default='INR')

        comments = models.TextField(null=True,blank=True)

        di1 = models.TextField(null=True,blank=True)
        di2 = models.TextField(null=True,blank=True)
        di3 = models.TextField(null=True,blank=True)
        di4 = models.TextField(null=True,blank=True)
        di5 = models.TextField(null=True,blank=True)
        di6 = models.TextField(null=True,blank=True)
        di7 = models.TextField(null=True,blank=True)
        di8 = models.TextField(null=True,blank=True)
        di9 = models.TextField(null=True,blank=True)
        di10 = models.TextField(null=True,blank=True)

        def __str__(self):
                return self.vendor.name + ' - ' + self.vendor_contact_person.name 

class VPOLineitems(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        vpo = models.ForeignKey(VPO,related_name='vpo_lineitems',on_delete=models.CASCADE)
        cpo_lineitem = models.ForeignKey(CPOLineitem,on_delete=models.CASCADE)
        
        product_title = models.CharField(max_length=200,null = False, blank = False)
        description = models.TextField(null=False, blank=False)
        model = models.CharField(max_length=200,null = True, blank = True)
        brand = models.CharField(max_length=200,null = True, blank = True)
        product_code = models.CharField(max_length=200,null = True, blank = True)
        
        hsn_code = models.CharField(max_length=10,null = True, blank = True)
        pack_size = models.CharField(max_length=10,null = True, blank = True)
        gst = models.FloatField(null = True, blank = True)
        uom = models.CharField(max_length=20,null = False, blank = False, default='Pcs')
        quantity = models.FloatField(null = False, blank = False)
        unit_price = models.FloatField(null = False, blank = False)

        discount = models.FloatField(default=0,null=True,blank=True)

        def __str__(self):
                return self.vpo.vendor.name + ' - ' + self.product_title