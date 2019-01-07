from django.urls import path,include
from rest_framework import routers
from .views import *

urlpatterns = [
    #Employee Portion
    path('claim_types/',ClaimTypesViewSet.as_view()),
    path('new_claim/',NewClaimViewSet.as_view()),
    path('new_claim/<id>/',NewClaimViewSet.as_view()),

    #Manager Portion
    
]