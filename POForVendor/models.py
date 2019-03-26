from django.db import models
from POFromCustomer.models import *
from Supplier.models import *
import uuid

class VendorPO(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        cpo = models.ForeignKey(CustomerPO,on_delete=models.CASCADE)
        vendor = models.ForeignKey(SupplierProfile,on_delete=models.CASCADE)
        vendor_contact_person = models.ForeignKey(SupplierContactPerson,on_delete=models.CASCADE)

        offer_reference =  models.CharField(max_length=100,null=True,blank=True)
        offer_date = models.DateField(null=True,blank=True)

        billing_address = models.TextField(null=True,blank=True)
        shipping_address = models.TextField(null=True,blank=True)
        delivery_date = models.DateField(null=True, blank=True)

        requester = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
        
        receiver_name = models.CharField(max_length = 200, null=True, blank=True)
        receiver_phone1 = models.CharField(max_length = 20, null=True, blank=True)
        receiver_phone2 = models.CharField(max_length = 20, null=True, blank=True)
        receiver_dept = models.CharField(max_length = 50, null=True, blank=True)

        payment_term = models.IntegerField(default=0)
        advance_percentage = models.IntegerField(default=0)

        freight_charges = models.FloatField(default = 0.0)
        custom_duties = models.FloatField(default = 0.0)
        pf = models.FloatField(default = 0.0)
        insurance = models.FloatField(default = 0.0)
        
        mode_of_transport = models.CharField(max_length=200,null=True,blank=True)
        inco_terms = models.CharField(max_length=200,null=True,blank=True)
        installation = models.CharField(max_length=200,null=True,blank=True)
        terms_of_payment = models.CharField(max_length=200,null=True,blank=True)

        currency = models.CharField(max_length=20,default='INR')

        comments = models.TextField(null=True,blank=True)

        po_status = models.CharField(max_length = 50, default='Preparing')

        di1 = models.TextField(default = '1.Original Invoice & Delivery Challans Four (4) copies each must be submitted at the time of delivery of goods')
        di2 = models.TextField(default = '2.Entire Goods must be delivered in Single Lot if not specified otherwise. For any changes, must inform IMMEDIATELY.')
        di3 = models.TextField(default = '3.Product Specifications, Qty, Price, Delivery Terms are in accordance with your offer')
        di4 = models.TextField(default = '4.Product Specifications, Qty, Price, Delivery Terms shall remain unchanged for this order.')
        di5 = models.TextField(default = '5.Notify any delay in shipment as scheduled IMMEDIATELY.')
        di6 = models.TextField(default = '6.Mail all correspondance to corporate office address only.')
        di7 = models.TextField(default = '7.Must Submit Warranty Certificate, PO copy, TC copy (if any) and all other documents as per standard documentation')
        di8 = models.TextField(null=True,blank=True)
        di9 = models.TextField(null=True,blank=True)
        di10 = models.TextField(null=True,blank=True)

        def __str__(self):
                return self.vendor.name + ' - ' + self.vendor_contact_person.name 

class VendorPOTracker(models.Model):
        po_number = models.CharField(primary_key=True, max_length=20, unique = True)
        po_date = models.DateField(auto_now_add=True)
        status = models.CharField(max_length=50, default='Requested')

        vpo = models.ForeignKey(VendorPO,on_delete=models.CASCADE)
        requester = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

        def __str__(self):
                return self.po_number + '  -  ' + str(self.po_date)

class VendorPOLineitems(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        vpo = models.ForeignKey(VendorPO,related_name='vpo_lineitems',on_delete=models.CASCADE)
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