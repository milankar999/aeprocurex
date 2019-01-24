from django.urls import path
from Employee.views import *

urlpatterns = [
    path('',user_login,name='default_login'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('success/',success,name='success'),
    path('crm_home/',crm_home_load,name='crm_home_load'),
    path('sourcing_home/',sourcing_home_load,name='sourcing_home_load'),
    path('sales_home/',sales_home_load,name='sales_home_load'),

    #API Urls
    path('api/login/',LoginView.as_view()),
    path('api/logout/',LogoutView),
]