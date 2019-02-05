from django.urls import path
from .views import *

urlpatterns = [
    path('new_expence/apply/',new_expence_apply,name='new-expence-apply'),
    path('apply_list/',expence_apply_list,name='expence-apply-list'),
]   
