from .models import institutions,pic_institutions,pic_institution_data_changes,institution_data_changes,institution_verifications,institution_types
from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.Account.models import *

class institutionTypesSerializer (serializers.ModelSerializer):
    class Meta: 
        model = institution_types
        fields = "__all__"

class institutionSerializer (serializers.ModelSerializer):
    institution_type_name = serializers.CharField(source='institution_type_id.name', read_only=True)
    class Meta: 
        model = institutions
        fields = "__all__"

class picInstitutionsSerializer (serializers.ModelSerializer):
    institution_name = serializers.CharField(source='institution_id.name', read_only=True)
    class Meta: 
        model = pic_institutions
        fields = "__all__"

class picUsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = pic_users
        fields = ['pic_id', 'email', 'password','is_yayasan', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

class logPicUserSerializer (serializers.ModelSerializer):
    action = serializers.CharField(default='2')
    class Meta:
        model = log_pic_users
        fields = ['id','action']

class institutionVerificationsSerializer (serializers.ModelSerializer):
    class Meta:
        model = institution_verifications
        fields = "__all__"

class PicUserLoginSerializer(serializers.Serializer):
    email =serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'},write_only=True)