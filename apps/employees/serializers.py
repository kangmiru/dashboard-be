from .models import *
from rest_framework import serializers
from apps.Account.models import *

class employeesSerializer (serializers.ModelSerializer):
    class Meta:
        model = employees
        fields = '__all__'
    
class employeeUsersSerializer (serializers.ModelSerializer):
    class Meta:
        model = employee_users
        fields = "__all__"
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        user = employee_users(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class employeeDataChangeSerializer (serializers.Serializer):
    class Meta:
        model = employee_data_changes
        fields = "__all__"

class employeeUserDataChangeSerializer (serializers.Serializer):
    class Meta:
        model = employee_user_data_changes
        fields = "__all__"
        extra_kwargs = {'password' : {'write_only' : True}}

class logEmployeeUserSerializer (serializers.Serializer):
    class Meta:
        model = log_employee_users
        fields = "__all__"

class EmployeeLoginSerializer(serializers.Serializer):
    email =serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'})