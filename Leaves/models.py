from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class ApplicableLeaves(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    leaves = models.FloatField(default=0)

    def __str__(self):
        return self.employee.first_name + ' ' + self.employee.last_name + ' ' + str(self.leaves)

@receiver(post_save,sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        ApplicableLeaves.objects.create(employee=instance)


class LeaveApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length = 20, null = True, blank = True)
    reason = models.TextField()
    start_date = models.DateField()
    no_of_days = models.FloatField()
    status = models.CharField(max_length=50,default='Requested')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee.first_name + ' - ' + self.employee.last_name + ' ' + str(self.start_date) + ' ' + str(self.no_of_days) 

