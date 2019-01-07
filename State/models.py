from django.db import models

class StateList(models.Model):
    state_name = models.CharField(max_length=100 ,primary_key = True)

    def __str__(self):
        return self.state_name
