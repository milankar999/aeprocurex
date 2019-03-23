from django.db import models
import uuid

class BankAccountList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bank_name = models.CharField(max_length=200)
    account_holder = models.CharField(max_length=200)
    ifcs_code = models.CharField(max_length = 200)

    def __str__(self):
        return self.bank_name + ' : ' + self.account_holder + ' : ' + self.ifcs_code