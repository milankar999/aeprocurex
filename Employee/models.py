from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length = 50, null=True,blank=True)
    hr_user_type = models.CharField(max_length = 50, null=True,blank=True)
    claim_user_type = models.CharField(max_length = 50, default = 'user')
    supplier_payment_user_type = models.CharField(max_length = 50, default = 'user')
    cpo_editing = models.CharField(max_length = 50, default = 'no')
    rfp_editing = models.CharField(max_length = 50, default = 'no')
    creating_customer = models.CharField(max_length = 50, default = 'no')
    customer_editing = models.CharField(max_length = 50, default = 'no')
    designation = models.CharField(max_length=50, null = True, blank = True)
    personal_email = models.CharField(max_length=100, null = True, blank = True)
    office_email = models.CharField(max_length=100, null = True, blank = True)
    personal_mobile = models.CharField(max_length=100, null = True, blank = True)
    optional_personal_mobile = models.CharField(max_length=100, null = True, blank = True)
    office_mobile = models.CharField(max_length=100, null = True, blank = True)
    blood_group = models.CharField(max_length=10, null = True, blank = True)
    joining_date = models.DateTimeField(null = True, blank = True)
    leaving_date = models.DateTimeField(null = True, blank = True)
    

    class Meta:
        ordering = ('-designation',)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


@receiver(post_save,sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()