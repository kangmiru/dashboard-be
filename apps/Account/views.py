# from rest_framework import permissions, viewsets, status
# from django.contrib.auth.hashers import make_password
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework_simplejwt.tokens import RefreshToken
# from http import HTTPMethod
# from utils.format import format_number
# from utils.jwt import decode_jwt
# from .helper import get_user_from_jwt
# from .serializer import LoginSerializer, PICSerializer, UserSerializer, RoleSerializer
# from .modelsV2 import PersonInCharge, User, Role
# from apps.institutions.models import institutions
# from utils.format import convert_to_title_case
# from rest_framework_simplejwt.token_blacklist.models import (
#     BlacklistedToken,
#     OutstandingToken,
# )
# from rest_framework_simplejwt.tokens import UntypedToken
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


# class AuthenticationViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]

#     @action(
#         detail=False,
#         methods=[HTTPMethod.POST],
#         url_path="api/auth/login",
#         permission_classes=[permissions.AllowAny],
#     )
#     def login(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(
#         detail=False,
#         methods=[HTTPMethod.POST],
#         url_path="api/auth/logout",
#         permission_classes=[permissions.IsAuthenticated],
#     )
#     def logout(self, request):
#         try:
#             refresh_token = request.data.get("refresh")
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"detail": "Soccessfully logout"}, status=status.HTTP_200_OK)

#     @action(detail=False, methods=[HTTPMethod.POST])
#     def verify_token(self, request, *args, **kwargs):
#         token = request.data.get("token")
#         if not token:
#             return Response(
#                 {"detail": "No token provided."}, status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             # This will verify the token's validity and check for expiration
#             UntypedToken(token)

#             # Check if the token is blacklisted
#             outstanding_token = OutstandingToken.objects.get(token=token)
#             token_id = outstanding_token.id
#             if BlacklistedToken.objects.filter(token=token_id).exists():
#                 raise InvalidToken("Token is blacklisted")

#             return Response({"detail": "Token is valid."})

#         except TokenError as e:
#             # Handles expired and invalid tokens
#             return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

#     @action(detail=False, methods=[HTTPMethod.GET])
#     def get_role(self, request):
#         auth_header = request.META.get("HTTP_AUTHORIZATION")
#         if auth_header is not None:
#             tokens = auth_header.split()[1]
#             user = get_user_from_jwt(tokens)
#             serialier = RoleSerializer(user.role)
#             return Response(serialier.data, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "No Auth Token Found"}, status=status.HTTP_403_OK)

#     @action(detail=False, methods=[HTTPMethod.GET])
#     def user_info(self, request):
#         auth_header = request.META.get("HTTP_AUTHORIZATION")
#         if auth_header is not None:
#             tokens = auth_header.split()[1]
#             user = get_user_from_jwt(tokens)
#             return Response(
#                 {
#                     "id": user.id,
#                     "name": user.name,
#                     "role": user.role.name,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 {"error": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by("created_at")
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class PICViewSet(viewsets.ModelViewSet):
#     queryset = PersonInCharge.objects.all().order_by("created_at")
#     serializer_class = PICSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     @action(detail=False, methods=[HTTPMethod.POST])
#     def create(self, request):
#         try:
#             data = request.data
#             institution = institutions.objects.get(id=data["institution"])
#             institution_name = institution.institution_type.name
#             role_name = "penanggung_jawab_" + institution_name.lower()
#             role = Role.objects.get(name=role_name)
#             # Check if the user already exists to handle the unique email constraint
#             if User.objects.filter(email=data["email"]).exists():
#                 return Response(
#                     {
#                         "error": "Failed to create user",
#                         "message": "Email already exists",
#                     },
#                     status=status.HTTP_409_CONFLICT,
#                 )

#             # Since the user does not exist, create a new user
#             user = User(
#                 name=data["name"],
#                 email=data["email"],
#                 phone_number=data["phone_number"],
#                 role=role,
#             )
#             user.password = make_password(data["password"])  # Hash the password
#             user.save()

#             # Set user as person in charge for specific institution
#             PersonInCharge.objects.create(user=user, institution=institution)

#             return Response(
#                 {"message": "User created successfully"}, status=status.HTTP_201_CREATED
#             )
#         except Exception as e:
#             return Response(
#                 {"error": "Failed to create User", "message": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     @action(detail=False, methods=[HTTPMethod.PUT])
#     def update(self, request, pk=None):
#         try:
#             data = request.data
#             user = User.objects.get(id=pk)
#             user.name = data["name"]
#             user.email = data["email"]
#             user.phone_number = data["phone_number"]
#             if "pasword" in data:
#                 user.set_password(data["password"])
#             user.save()
#             pic = PersonInCharge.objects.get(user=user)
#             institution = institutions.objects.get(id=data["institution"])
#             pic.institution = institution
#             pic.save()
#             return Response(
#                 {"message": "User updated successfully"}, status=status.HTTP_200_OK
#             )
#         except Exception as e:
#             return Response(
#                 {"error": "Failed to update User", "message": str(e)},
#                 status=status.HTTP_200_OK,
#             )

#     @action(detail=False, methods=[HTTPMethod.GET])
#     def pic_list(self, request):
#         if request.query_params.get("count") == "true":
#             count_pic = self.get_queryset().count()
#             return Response({"context": "Penanggung Jawab", "count": count_pic})
#         pic_users = self.get_queryset()
#         page = self.paginate_queryset(pic_users)
#         serializer = self.serializer_class(page, many=True)
#         return self.get_paginated_response(serializer.data)

#     @action(detail=True, methods=[HTTPMethod.GET])
#     def pic_stats(self, request):
#         pic_yayasan_count = (
#             self.get_queryset()
#             .filter(institution__institution_type__name="Yayasan")
#             .count()
#         )
#         pic_sekolah_count = (
#             self.get_queryset()
#             .filter(institution__institution_type__name="Sekolah")
#             .count()
#         )
#         stats_data = [
#             {
#                 "name": "Yayasan",
#                 "value": pic_yayasan_count,
#                 "percentage": format_number(
#                     pic_yayasan_count / (pic_sekolah_count + pic_yayasan_count) * 100,
#                 ),
#             },
#             {
#                 "name": "Sekolah",
#                 "value": pic_sekolah_count,
#                 "percentage": format_number(
#                     pic_sekolah_count / (pic_sekolah_count + pic_yayasan_count) * 100,
#                 ),
#             },
#         ]
#         return Response(stats_data, status=status.HTTP_200_OK)

#     @action(detail=True, methods=[HTTPMethod.GET])
#     def get_pic_institution(self, request):
#         auth_header = request.META.get("HTTP_AUTHORIZATION")
#         if auth_header is not None:
#             tokens = auth_header.split()[1]
#             user = get_user_from_jwt(tokens)
#             pic = PersonInCharge.objects.get(user=user)
#             institution = pic.institution
#             extracted_address = institution.address.__str__().split(",")
#             province = extracted_address[-1:][0].strip().split(" ")[0]
#             city_regency = extracted_address[-2:][0].strip()
#             return Response(
#                 {
#                     "id": institution.id,
#                     "name": institution.name,
#                     "address": f"{city_regency}, {province}",
#                 },
#                 status=status.HTTP_200_OK,
#             )
