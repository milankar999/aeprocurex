from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class FirstClaimTypes(models.Model):
    claim_type1 = models.CharField(max_length = 200, primary_key = True) 

    def __str__(self):
        return self.claim_type1

class SecondClaimTypes(models.Model):
    claim_type2 = models.CharField(max_length = 200, primary_key = True)
    claim_type1 = models.ForeignKey(FirstClaimTypes, on_delete = models.CASCADE)

    def __str__(self):
        return self.claim_type2

class ThirdClaimTypes(models.Model):
    claim_type3 = models.CharField(max_length = 200, primary_key = True)
    claim_type2 = models.ForeignKey(SecondClaimTypes, on_delete = models.CASCADE)

    def __str__(self):
        return self.claim_type3

class ClaimDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    claim_type = models.ForeignKey(ThirdClaimTypes, on_delete = models.CASCADE)
    description = models.TextField(null=False,blank=False)
    total_basic_amount = models.FloatField(null=False,blank=False)
    applicable_gst_value = models.FloatField(null=False,blank=False, default = 0)
    date = models.DateField()
    document = models.FileField(upload_to='claim/',null=True,blank=True)

    status = models.CharField(max_length=200,default='Requested')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at) + self.employee.first_name  + ' - ' + self.employee.last_name 
