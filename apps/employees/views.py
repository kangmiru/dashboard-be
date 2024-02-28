from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, action

from .permissions import NotLoggedIn

from apps.Account.models import *

from .models import (
    employees,
)

from .serializers import (
    employeeUsersSerializer,
    employeesSerializer, 
    logEmployeeUserSerializer,
    EmployeeLoginSerializer,
)

class EmployeesView(viewsets.ModelViewSet):
    serializer_class = employeesSerializer
    @authentication_classes([TokenAuthentication])

    def get_queryset(self):
        return employees.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = employeesSerializer(queryset, many=True)

        data = queryset.values('id','nik','name','status')

        return Response({'data':data}, status=status.HTTP_200_OK)
    
    def create(self, request):
        if request.user.is_staff :
            serializer = employeesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'data berhasil ditambahkan', 'data' : serializer.data}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else :
            return Response({'message': 'Anda tidak memiliki izin untuk menambahkan data.'}, status=status.HTTP_403_FORBIDDEN)
        
class EmployeeLoginView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = EmployeeLoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        serializer = EmployeeLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)

                # generate token
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                
                if user.is_staff:
                    log_employee_users.objects.create(employee_user_id=user, action='1')
                else :
                    log_pic_users.objects.create(pic_id=user, action='1')

                return Response({'message': 'Login berhasil', 'access_token': access_token}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Email atau password salah'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class EmployeeLogoutView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = logEmployeeUserSerializer

    def logout(self, request):
        user = request.user
        logout(request)

        if user.is_staff:
            log_employee_users.objects.create(employee_user_id=user, action='2')
        else :
            log_pic_users.objects.create(pic_id=user, action='2')

        return Response({'message':'logout berhasil'}, status=status.HTTP_200_OK)
    
class EmployeeUserView(viewsets.ModelViewSet):
    serializer_class = employeeUsersSerializer
    @authentication_classes([TokenAuthentication])

    def get_queryset(self):
        return employee_users.objects.all()
    
    def list(self,request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = self.get_queryset()
        admin = queryset.filter(is_staff = True)
        serializer = employeeUsersSerializer(admin, many=True)

        if not queryset:
            return Response({'message':'belum ada data'})
        
        return Response(serializer.data)
    
    def create(self, request):
        if request.user.is_staff:
            serializer = employeeUsersSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'data berhasil disimpan', 'data':serializer.data}, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'messege':'anda tidak memiliki izin untuk menambahkan data'}, status=status.HTTP_401_UNAUTHORIZED)
        