from django.db import models
from django.contrib.auth.models import User
from Customer.models import *
import uuid


class RFPCreationDetail(models.Model):
    id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return  self.created_by.username + '    ' + str(self.creation_date)

class RFPApprovalDetail(models.Model):
    id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
    approved_date = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return str(self.approved_date) + '     ' + self.approved_by.username

class RFPKeyAccountsDetail(models.Model):
    id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
    key_accounts_manager = models.ForeignKey(User,on_delete = models.CASCADE)
    
    def __str__(self):
        return self.key_accounts_manager.username 

class RFPAssign1(models.Model):
    id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
    assign_to1 = models.ForeignKey(User,on_delete = models.CASCADE)
    
    def __str__(self):
        return self.assign_to1.username 

class RFPAssign2(models.Model):
    id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
    assign_to2 = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return self.assign_to2.username 

class RFPAssign3(models.Model):
    id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
    assign_to3 = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return self.assign_to3.username 

class RFPSourcingDetail(models.Model):
    id = models.CharField(max_length=200, null = False, blank = False, primary_key=True)
    completion_date = models.DateTimeField(auto_now_add=True)
    sourcing_completed_by = models.ForeignKey(User,null=True,blank = True,on_delete = models.CASCADE)

    def __str__(self):
        return str(self.completion_date) + '     ' + self.sourcing_completed_by.username 

class RFP(models.Model):
    rfp_no = models.CharField(max_length=200,null = False, blank = False, primary_key=True)
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    customer_contact_person = models.ForeignKey(CustomerContactPerson,on_delete=models.CASCADE)
    end_user = models.ForeignKey(EndUser,null=True,blank=True,on_delete=models.CASCADE)
    reference = models.CharField(max_length=200,null = False, blank = False)
    opportunity_status = models.CharField(max_length=100)
    enquiry_status = models.CharField(max_length=100)
    closing_reason = models.TextField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)

    rfp_creation_details = models.ForeignKey(RFPCreationDetail,on_delete = models.CASCADE,null=True, blank=True)
    rfp_approval_details = models.ForeignKey(RFPApprovalDetail,on_delete = models.SET_NULL,null=True, blank=True)
    rfp_keyaccounts_details = models.ForeignKey(RFPKeyAccountsDetail,on_delete = models.SET_NULL,null=True, blank=True)
    rfp_assign1 = models.ForeignKey(RFPAssign1,on_delete = models.SET_NULL,null=True, blank=True)
    rfp_assign2 = models.ForeignKey(RFPAssign2,on_delete = models.SET_NULL,null=True, blank=True)
    rfp_assign3 = models.ForeignKey(RFPAssign3,on_delete = models.SET_NULL,null=True, blank=True)
    rfp_sourcing_detail = models.ForeignKey(RFPSourcingDetail,on_delete = models.SET_NULL,null=True, blank=True)

    rfp_type = models.CharField(max_length=200,default='Regular')
    creation_type = models.CharField(max_length=200,default='DEP')

    single_vendor_approval = models.CharField(max_length=10,default='No')
    single_vendor_reason = models.TextField(null=True,blank=True)

    current_sourcing_status = models.CharField(max_length = 200, default = 'Not Mentioned')

    #attachment
    document1 = models.FileField(upload_to='rfp/',null=True,blank=True)
    document2 = models.FileField(upload_to='rfp/',null=True,blank=True)
    document3 = models.FileField(upload_to='rfp/',null=True,blank=True)
    document4 = models.FileField(upload_to='rfp/',null=True,blank=True)
    document5 = models.FileField(upload_to='rfp/',null=True,blank=True)

    def __str__(self):
        return self.rfp_no + '     ' + self.customer.name

class RFPLineitem(models.Model):
    rfp_no = models.ForeignKey(RFP,null=True,blank=True,on_delete=models.CASCADE)
    lineitem_id = models.CharField(max_length=200,null = False, blank = False, primary_key=True)
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
    target_price = models.FloatField(null = True, blank = True)
    remarks = models.TextField(max_length=200,null = True, blank = True)
    customer_lead_time = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to = 'pic_folder/', blank = True, default = 'pic_folder/None/no-img.jpg')

    creation_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return self.lineitem_id+ '  ' +  self.product_title

class RFPStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfp = models.ForeignKey(RFP, on_delete = models.CASCADE)
    status = models.CharField(max_length=200)

    update_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return str(self.rfp.rfp_no) + '     ' + self.status 