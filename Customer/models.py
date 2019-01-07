from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    id = models.CharField(max_length=50 ,primary_key = True)
    name = models.CharField(max_length=200,null = False, blank = False)
    location = models.CharField(max_length=200,null = True, blank = True)
    code = models.CharField(max_length=20,null = False, blank = False, unique=True)
    address = models.TextField(null = True, blank = True)
    city = models.CharField(max_length=100,null = True, blank = True)
    state = models.CharField(max_length=100,null = True, blank = True)
    pin = models.CharField(max_length=20,null = True, blank = True)
    country = models.CharField(max_length=100,null = True, blank = True)
    office_email1 = models.EmailField(max_length=100,null = True, blank = True)
    office_email2 = models.EmailField(max_length=100,null = True, blank = True)
    office_phone1 = models.CharField(max_length=20,null = True, blank = True)
    office_phone2 = models.CharField(max_length=20,null = True, blank = True)
    gst_number = models.CharField(max_length=20,null = True, blank = True, default=None)
    vendor_code = models.CharField(max_length=20,null = True, blank = True)
    payment_term = models.IntegerField(null=True, blank=True)
    inco_term = models.CharField(max_length=50, null=True, blank = True)
    tax_type = models.CharField(max_length=50,null=True, blank=True,default='Normal')

    billing_address = models.TextField(null=True,blank=True,default='Same')
    shipping_address = models.TextField(null=True,blank=True,default='Same')
    
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + self.location

    @property
    def CustomerContactPerson(self):
        return self.CustomerContactPerson_set.all()

    @property
    def EndUser(self):
        return self.EndUser_set.all()

class CustomerContactPerson(models.Model):
    id = models.CharField(max_length=50 ,primary_key = True)
    name = models.CharField(max_length=200,null = False, blank = False)
    mobileNo1 = models.CharField(max_length=20,null = True, blank = True)
    mobileNo2 = models.CharField(max_length=20,null = True, blank = True)
    email1 = models.EmailField(max_length=50,null = True, blank = True)
    email2 = models.EmailField(max_length=50,null = True, blank = True)   

    customer_name = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + self.customer_name.name + ' - ' + self.customer_name.location

class EndUser(models.Model):
    id = models.CharField(max_length=50 ,primary_key = True)    
    user_name = models.CharField(max_length=200,null = False, blank = False)
    department_name = models.CharField(max_length=200,null = False, blank = False)
    mobileNo1 = models.CharField(max_length=20,null = True, blank = True)
    mobileNo2 = models.CharField(max_length=20,null = True, blank = True)
    email1 = models.EmailField(max_length=100,null = True, blank = True)
    email2 = models.EmailField(max_length=100,null = True, blank = True)

    customer_name = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name + ' - ' + self.customer_name.name