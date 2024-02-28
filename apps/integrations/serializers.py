from .models import institution_school_verifications, institution_schools, integrations
from rest_framework import serializers

class institutionSchoolVerSerializer (serializers.ModelSerializer):
    class Meta:
        model = institution_school_verifications
        fields = "__all__"

class institutionSchoolsSerializer (serializers.ModelSerializer):
    sekolah = serializers.CharField(source='school_id.name',read_only=True)
    yayasan = serializers.CharField(source='institution_id.name',read_only=True)
    penanggung_jawab = serializers.CharField(source='created_by.name',read_only=True)
    class Meta:
        model = institution_schools
        fields = "__all__"

class integrationsSerializer (serializers.ModelSerializer):
    class Meta:
        model = integrations
        fields = "__all__"