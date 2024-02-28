import calendar
from datetime import datetime
import logging
from django.http import Http404
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, action
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

from apps.Account.models import *
from apps.employees.serializers import employeeUsersSerializer, EmployeeLoginSerializer,logEmployeeUserSerializer
from apps.schools.models import *
from apps.schools.serializers import *

from .serializers import (
    institutionSerializer,
    institutionTypesSerializer,
    picInstitutionsSerializer,
    picUsersSerializer,
    logPicUserSerializer,
    PicUserLoginSerializer,
)

from .models import (
    institutions,
    institution_types,
    pic_institutions,
)

class InstitutionViews(viewsets.ModelViewSet):
    serializer_class = institutionSerializer
    @authentication_classes([TokenAuthentication])

    def get_queryset(self):
        queryset = institutions.objects.all()
        limit = self.request.query_params.get('limit', None)
        offset = self.request.query_params.get('offset', None)
        type = self.request.query_params.get('type', None)
        name = self.request.query_params.get('name',None)

        if name is not None:
            queryset = queryset.filter(name__icontains=str(name))

        if type is not None:
            queryset = queryset.filter(institution_type_id__name__iexact=str(type))
        
        if limit is not None :
            if offset is None :
                queryset = queryset[:int(limit)] 
            else :
                queryset = queryset[int(offset):int(limit)]
        
        count = queryset.count()
        
        return (queryset,count)
     
    def list_total(self, request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki akses'}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = institutions.objects.all()
        sekolah = schools.objects.count()
        count = self.get_queryset()[1]
        serializer = institutionSerializer(queryset, many=True)

        count_yayasan = queryset.filter(institution_type_id__name='Yayasan').count()
        count_sekolah = queryset.filter(institution_type_id__name='Sekolah').count()

        response = {
            'yayasan':count_yayasan,
            'sekolah':sekolah,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def list(self,request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki akses'}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = institutions.objects.all()
        count = self.get_queryset()[1]
        serializer = institutionSerializer(queryset, many=True)

        count_yayasan = queryset.filter(institution_type_id__name='Yayasan').count()
        count_sekolah = queryset.filter(institution_type_id__name='Sekolah').count()

        response = {
            "list_sekolah_yayasan" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def list_yayasan(self,request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki akses'}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = institutions.objects.all()
        count = self.get_queryset()[1]
        serializer = institutionSerializer(queryset, many=True)

        count_yayasan = queryset.filter(institution_type_id__name='Yayasan')
        count_sekolah = queryset.filter(institution_type_id__name='Sekolah').count()
        serializer = institutionSerializer(count_yayasan, many=True)

        response = {
            "list_yayasan" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def list_sekolah(self,request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki akses'}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = schools.objects.all()

        serializer = schoolsSerializer(queryset, many=True)

        response = {
            "list_sekolah" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
     
    def create(self, request):
        if request.user.is_staff:
            serializer = institutionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'data berhasil disimpan'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'message':'anda tidak memiliki akses'}, status=status.HTTP_401_UNAUTHORIZED)
     
    def retrieve(self, request, pk = None):
        if request.user.is_staff:
            queryset = self.get_queryset()[0]
            institution = get_object_or_404(queryset, pk=pk)
            serializer = institutionSerializer(institution)
            response = {
                "message" : "detail institusi berhasil didapatkan",
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'message':'anda tidak hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
     
    def update(self, request, pk = None):
        if request.user.is_staff:
            queryset = self.get_queryset()[0]
            institution = get_object_or_404(queryset, pk=pk)
            serializer = institutionSerializer(institution, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message':'data berhasil diubah'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
     
    def destroy(self, request, pk = None):
        if request.user.is_staff:
            queryset = self.get_queryset()[0]
            institusi = get_object_or_404(queryset, pk=pk)
            serializer = institutionSerializer(institusi)

            institusi.delete()

            return Response({'message':'data berhasil dihapus'}, status=status.HTTP_200_OK)
        
        else:
            return Response({'message':'anda tidak memilik hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
     
class institutionTypeViews(viewsets.ModelViewSet):
    serializer_class = institutionTypesSerializer
    # permission_classes = [IsAuthenticated]
    @authentication_classes([TokenAuthentication])
     
    def get_queryset(self):
        queryset = institution_types.objects.all()
        limit = self.request.query_params.get('limit', None)
        offset = self.request.query_params.get('offset', None)
        
        if limit is not None :
            if offset is None :
                queryset = queryset[:int(limit)] 
            else :
                queryset = queryset[int(offset):int(limit)]
        
        return queryset
     
    def list(self,request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        jumlahData = self.get_queryset().count()
        queryset = self.get_queryset()
        serializer = institutionTypesSerializer(queryset, many=True)
        response = {
            "jumlah_data" : jumlahData,
            "data" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
     
     
    def create(self, request):
        if request.user.is_staff:
            serializer = institutionTypesSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message':'data berhasil disimpan'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
     
class picInstitutionsView(viewsets.ModelViewSet):
    serializer_class = picInstitutionsSerializer
    # permission_classes = [IsAuthenticated]
    @authentication_classes([TokenAuthentication])

    def get_queryset(self):
        return pic_institutions.objects.all()
     
    def list(self, request, pk=None):
        if request.user.is_staff:
            # yayasan = institutions.objects.get(pk=pk)
            queryset = self.get_queryset()
            # if not yayasan :
            #     return Response({'message':'yayasan tidak terdaftar'})
            
            # sekolah = queryset.filter(institution_id = yayasan)
            sekolah = queryset.all()
            serializer = picInstitutionsSerializer(sekolah, many=True)
            response = {
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def create(self, request):
        if request.user.is_staff:
            serializer = picInstitutionsSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message':'data berhasil disimpan'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, pk=None):
        if request.user.is_staff:
            try:
                queryset = self.get_queryset().get(pk=pk)
                serializer = picInstitutionsSerializer(queryset)

                data = serializer.data

                return Response({'data':data}, status=status.HTTP_200_OK)
            except pic_institutions.DoesNotExist:
                return Response({'message':'terjadi kesalahan'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
     
    def update(self, request, pk = None):
        queryset = self.get_queryset().get(pk=pk)
        if request.user.is_staff:
            serializer = picInstitutionsSerializer(queryset, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message':'data berhasil diubah','data':serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else :
            return Response({'message':'anda tidak memiliki akses'}, status=status.HTTP_401_UNAUTHORIZED)
     
    def destroy(self, request, pk = None):
        queryset = self.get_queryset().get(pk=pk)
        if request.user.is_staff:
            serializer = picInstitutionsSerializer(queryset)
            
            queryset.delete()
            return Response({'message':'data berhasil dihapus'}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)

class picUserView (viewsets.ModelViewSet):
    serializer_class = picUsersSerializer
    # permission_classes = [IsAuthenticated]
    @authentication_classes([TokenAuthentication])

    def get_queryset(self):
        return pic_users.objects.all()
    
    def list(self, request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki akses'})
        
        queryset = self.get_queryset()
        serializer = picUsersSerializer(queryset, many=True)

        data = serializer.data

        return Response({'data':data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data.copy()
        data['password'] = make_password(data['password'])
        serializer = picUsersSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'berhasil menambahkan data'}, status=status.HTTP_200_OK)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    

class picUserLoginView (viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PicUserLoginSerializer

    def login(self, request, *args, **kwargs):
        serializer = PicUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = pic_users.objects.get(email=email)
            except user.DoesNotExist:
                return Response({'error': 'Email salah'}, status=401)
            
            if not check_password(password, user.password):
                return Response({'message':'password salah'})

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            log_pic_users.objects.create(pic_id=user, action='1')

            return Response({'message': 'login berhasil', 'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'email atau password salah'}, status=status.HTTP_401_UNAUTHORIZED)
        
class picUserLogOutView (viewsets.ModelViewSet):
    serializer_class = logPicUserSerializer
    
    def logout(self,request):
        user = request.user

        # Logout hanya jika user bukan AnonymousUser
        if not isinstance(user, AnonymousUser):
            logout(request)

            # Cek apakah user adalah instans dari model CostumUser
            if isinstance(user, CostumUser):  # Sesuaikan dengan model CostumUser yang sebenarnya
                log_pic_users.objects.create(pic_id=user, action='2')
            else:
                # Handle kasus lain jika diperlukan
                pass

            return Response({'message': 'logout berhasil'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Tidak ada user yang terautentikasi untuk logout'}, status=status.HTTP_400_BAD_REQUEST)

class picLoginStatisticsView (viewsets.ModelViewSet):
    serializer_class = logPicUserSerializer
    @authentication_classes([TokenAuthentication])
     
    def get_queryset(self):
        queryset = log_pic_users.objects.filter(
            action="1",
        )
        year = self.request.query_params.get('year', None)

        if not year:
            year = datetime.now().year

        queryset = queryset.filter(created_at__year=year)
        
        if queryset.filter(pic_id__is_yayasan=True).exists() or queryset.filter(pic_id__is_yayasan=False).exists():
            count = queryset.count()
        else:
            count = 'belum ada data'

        if queryset.filter(pic_id__is_yayasan=True).exists(): 
            count_yayasan = queryset.count()
        else:
            count_yayasan = 'belum ada data'
        
        if queryset.filter(pic_id__is_yayasan=False).exists():
            count_sekolah = queryset.count()
        else:
            count_sekolah = 'belum ada data'
        
        return (queryset,count, count_yayasan, count_sekolah)
     
    def list(self, request):
        if not request.user.is_staff:
            return Response(
                {"message": "Anda tidak dapat mengakses menu ini"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        queryset = self.get_queryset()[0]

        year = self.request.query_params.get('year', None)
        if not year:
            year = datetime.now().year

        queryset = queryset.filter(created_at__year=year)

        serializer = logPicUserSerializer(queryset,many=True)

        # countAll = queryset.count()
        count_yayasan = self.get_queryset()[2]
        count_sekolah = self.get_queryset()[3]

        monthly_stats = queryset.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id'))

        response = {
            "tahun": year,
            # "statistik_keseluruhan": countAll,
            'statistik yayasan':count_yayasan,
            'statistik sekolah':count_sekolah,
        }

        for stat in monthly_stats:
            response[f"statistik_{calendar.month_abbr[stat['month']].lower()}"] = stat['count']

        return Response(response, status=status.HTTP_200_OK)

