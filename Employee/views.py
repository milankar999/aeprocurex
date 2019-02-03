from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Profile

def user_login(request):
        try:
                u = User.objects.get(username=request.user)
                type = u.profile.type
                if type == 'Sales':
                        return render(request,"Sales/sales_home.html")

                if type == 'Sourcing':
                        return render(request,"Sourcing/Sourcing_home.html")

                if type == 'CRM':
                        return render(request,"CRM/crm_home.html")
        except:
                context={}
                if request.method=="POST":
                        username=request.POST['username']
                        password=request.POST['password']
                        user = authenticate(request, username = username, password = password)
                        if user:
                                login(request,user)
                                if request.GET.get('next',None):
                                        return HttpResponseRedirect(request.GET['next'])
                                return render(request,'Employee/Auth/success.html')
                        else:
                                context["error"] = "Please provide valid Credentials"
                                return render(request,'Employee/Auth/login.html',context)
                else:
                        return render(request,"Employee/Auth/login.html",context)

def user_logout(request):
    if request.method=="POST":
        logout(request)
        return HttpResponseRedirect(reverse('login'))

@login_required(login_url="/employee/login/")
def success(request):
    u = User.objects.get(username=request.user)
    type = u.profile.type
    
    if type == 'Sales':
        return render(request,"Sales/sales_home.html")

    if type == 'Sourcing':
        return render(request,"Sourcing/Sourcing_home.html")

    if type == 'CRM':
        return render(request,"CRM/crm_home.html")

@login_required(login_url="/employee/login/")
def crm_home_load(request):
    u = User.objects.get(username=request.user)
    type = u.profile.type
    if type == 'CRM':
        return render(request,"CRM/crm_home.html")

@login_required(login_url="/employee/login/")
def sourcing_home_load(request):
    u = User.objects.get(username=request.user)
    type = u.profile.type
    if type == 'Sourcing':
        return render(request,"Employee/sourcing_home.html")

@login_required(login_url="/employee/login/")
def sales_home_load(request):
    u = User.objects.get(username=request.user)
    type = u.profile.type
    if type == 'Sales':
        return render(request,"Employee/sales_home.html")


#API Views
from rest_framework.views import APIView
from .serializers import LoginSerializer
from django.contrib.auth import login as django_login, logout as django_logout 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


class LoginView(APIView):
        def post(self,request):
                serializer = LoginSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data["user"]
                django_login(request,user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token":token.key,"type":user.profile.type}, status = 200)

class LogoutView():
        authentication_classes=[TokenAuthentication, ]

        def post(self, request):
                django_logout(request)
                return Response(status = 204)
