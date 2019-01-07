from django.db import models
from django.contrib.auth.models import User

class SupplierProfile(models.Model):
    id = models.CharField(max_length=50 ,primary_key = True)
    name = models.CharField(max_length=200,null = False, blank = False)
    location = models.CharField(max_length=200,null = True, blank = True)
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
    payment_term = models.IntegerField(null=True, blank=True)
    advance_persentage = models.IntegerField(null=True, blank=True)
    inco_term = models.CharField(max_length=50, null=True, blank = True)

    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + self.location

    @property
    def SupplierContactPerson(self):
        return self.SupplierContactPerson_set.all()

class SupplierContactPerson(models.Model):
    id = models.CharField(max_length=50 ,primary_key = True)
    name = models.CharField(max_length=200,null = False, blank = False)
    mobileNo1 = models.CharField(max_length=20,null = True, blank = True)
    mobileNo2 = models.CharField(max_length=20,null = True, blank = True)
    email1 = models.EmailField(max_length=100,null = True, blank = True)
    email2 = models.EmailField(max_length=100,null = True, blank = True)   

    supplier_name = models.ForeignKey(SupplierProfile,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' - ' + self.supplier_name.name + ' - ' + self.supplier_name.location
