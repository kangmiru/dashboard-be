# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from apps.institutions.serializers import institutionSerializer
# from .modelsV2 import User, PersonInCharge, Role


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(email=data["email"], password=data["password"])
#         if user is None:
#             raise serializers.ValidationError("Invalid login credentials")

#         refresh = RefreshToken.for_user(user)
#         return {
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#         }


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "name", "email", "phone_number"]


# class PICSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     institution = serializers.SerializerMethodField()

#     class Meta:
#         model = PersonInCharge
#         fields = ["user", "institution"]

#     def get_institution(self, obj):
#         return {
#             "id": obj.institution.id,
#             "name": obj.institution.name,
#             "type": {
#                 "id": obj.institution.institution_type.id,
#                 "name": obj.institution.institution_type.name,
#             },
#         }


# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = ["name"]
