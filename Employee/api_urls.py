from django.urls import path
from Employee.views import *

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView),
]