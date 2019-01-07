from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name'
        ]
        read_only_fields = ('first_name','last_name',)

class ApplicableLeavesSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(many=False)
    class Meta:
        model = ApplicableLeaves
        
        #fields = '__all__'
        fields = (
            'id',
            'employee',
            'leaves'
        )
        read_only_fields = ('employee',)
        #depth = 1

class UserApplicableLeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicableLeaves
        
        #fields = '__all__'
        fields = (
            'id',
            'leaves'
        )

class NewLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        
        #fields = '__all__'
        fields = (
            'id',
            'employee',
            'leave_type',
            'reason',
            'start_date',
            'no_of_days'
        )
        read_only_fields = ('employee',)

class AppliedLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        
        fields = (
            'id',
            'leave_type',
            'reason',
            'start_date',
            'no_of_days',
            'status'
        )

class PendingApprovalLeaveSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(many=False)
    class Meta:
        model = LeaveApplication
        
        fields = (
            'id',
            'employee',
            'leave_type',
            'reason',
            'start_date',
            'no_of_days',
            'status'
        )

class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = (
            'id',
            'employee'
            )
        read_only_fields = ('employee',)

class AllLeaveApplicationSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(many=False)
    class Meta:
        model = LeaveApplication
        
        fields = (
            'id',
            'employee',
            'leave_type',
            'reason',
            'start_date',
            'no_of_days',
            'status'
        )