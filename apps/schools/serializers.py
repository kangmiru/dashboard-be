from .models import education_levels,schools
from rest_framework import serializers

class educationLevelsSerializer (serializers.ModelSerializer):
    class Meta:
        model = education_levels
        fields = "__all__"

class schoolsSerializer (serializers.ModelSerializer):
    education_level_name = serializers.CharField(source='education_level_id.name', read_only=True)
    class Meta:
        model = schools
        fields = "__all__"