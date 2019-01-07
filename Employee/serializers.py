from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        username = data.get("username","")
        password = data.get("password", "")

        if username and password:
            user =  authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg="Inactive User"
                    raise exceptions.ValidationError(msg)
            else:
                msg="Wrong Credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg="Must Provide Username and Password"
            raise exceptions.ValidationError(msg)
        return data