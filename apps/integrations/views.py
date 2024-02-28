from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes

from .models import (
    institution_schools,
    institution_school_verifications,
    integrations,
)

from .serializers import (
    institutionSchoolsSerializer,
    institutionSchoolVerSerializer,
    integrationsSerializer
)

from apps.institutions.models import *
from apps.institutions.serializers import *
from apps.schools.models import *

class institutionSchoolView(viewsets.ModelViewSet):
    serializer_class = institutionSchoolsSerializer
    # permission_classes = [IsAuthenticated]
    @authentication_classes([TokenAuthentication])

    def get_queryset(self):
        queryset = institution_schools.objects.all()
        limit = self.request.query_params.get('limit', None)
        offset = self.request.query_params.get('offset', None)
        
        if limit is not None :
            if offset is None :
                queryset = queryset[:int(limit)] 
            else :
                queryset = queryset[int(offset):int(limit)]
        
        return queryset
     
    def list(self, request):
        if request.user.is_staff:
            jumlahData = self.get_queryset().count()
            queryset = self.get_queryset()
            serializer = institutionSchoolsSerializer(queryset, many=True)
            response = {
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
            
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def create(self, request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = institutionSchoolsSerializer(data = request.data)

        if serializer.is_valid(raise_exception= True):
            serializer.save()
            response = {
                "message" : "data baru telah ditambahkan",
                "data" : serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk = None):
        if request.user.is_staff:
            queryset = self.get_queryset()
            insSch = get_object_or_404(queryset, pk=pk)
            serializer = institutionSchoolsSerializer(insSch)
            response = {
                "message" : "detail berhasil didapatkan",
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def view_yayasan(self, request, pk=None):
        if request.user.is_yayasan or request.user.is_staff:
            yayasan = institutions.objects.get(pk=pk)
            queryset = institution_schools.objects.all()

            if not yayasan : 
                return Response({'message':'yayasan tidak terdaftar'})
            
            sekolah = queryset.filter(institution_id = yayasan)
            menengah_atas = queryset.filter(school_id__education_level_id__name = 'SMA', institution_id = yayasan).count()
            menengah_pertama = queryset.filter(school_id__education_level_id__name = 'SMP', institution_id = yayasan).count()
            dasar = queryset.filter(school_id__education_level_id__name = 'SD', institution_id = yayasan).count()
            kejuruan = queryset.filter(school_id__education_level_id__name = 'SMK', institution_id = yayasan).count()
            aliyah = queryset.filter(school_id__education_level_id__name = 'MA', institution_id = yayasan).count()
            tsanawiyah = queryset.filter(school_id__education_level_id__name = 'MTS', institution_id = yayasan).count()
            ibtidaiyah = queryset.filter(school_id__education_level_id__name = 'MI', institution_id = yayasan).count()
            serializer = institutionSchoolsSerializer(sekolah, many=True)
            response = {
                "SMA" : menengah_atas,
                "SMP" : menengah_pertama,
                "SD" : dasar,
                "SMK" : kejuruan,
                "MA" : aliyah,
                "MTS" : tsanawiyah,
                "MI" : ibtidaiyah,
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def view_sekolah(self, request, pk=None, name=None):
        if request.user.is_yayasan or request.user.is_staff:
            yayasan = institutions.objects.get(pk=pk)
            tingkat = education_levels.objects.get(name=name)
            queryset = institution_schools.objects.all()

            if not yayasan : 
                return Response({'message':'yayasan tidak terdaftar'})
            
            sekolah = queryset.filter(institution_id = yayasan,school_id__education_level_id__name =tingkat)
            serializer = institutionSchoolsSerializer(sekolah, many=True)
            response = {
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
     
    def update(self, request, pk = None):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = self.get_queryset()
        insSch = get_object_or_404(queryset, pk=pk)
        serializer = institutionSchoolsSerializer(insSch, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message" : "data berhasil diupdate"
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class institutionSchoolVerView(viewsets.ModelViewSet):
    serializer_class = institutionSchoolVerSerializer
    @authentication_classes([TokenAuthentication])
    def get_queryset(self):
        queryset = institution_school_verifications.objects.all()
        limit = self.request.query_params.get('limit', None)
        offset = self.request.query_params.get('offset', None)
       
        if limit is not None :
            if offset is None :
                queryset = queryset[:int(limit)] 
            else :
                queryset = queryset[int(offset):int(limit)]
        
        return queryset
     
    def list(self, request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        jumlahData = self.get_queryset().count()
        queryset = self.get_queryset()
        serializer = institutionSchoolVerSerializer(queryset, many=True)
        response = {
            "data" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = institutionSchoolVerSerializer(data = request.data)

        if serializer.is_valid(raise_exception= True):
            serializer.save()
            response = {
                "message" : "data baru telah ditambahkan",
                "data" : serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk = None):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = self.get_queryset()
        insSchVer = get_object_or_404(queryset, pk=pk)
        serializer = institutionSchoolVerSerializer(insSchVer)
        response = {
            "message" : "detail berhasil didapatkan",
            "data" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
     
     
    def update(self, request, pk = None):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = self.get_queryset()
        insSchVer = get_object_or_404(queryset, pk=pk)
        serializer = institutionSchoolVerSerializer(insSchVer, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message" : "data berhasil diupdate"
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class integrationView(viewsets.ModelViewSet):
    serializer_class = integrationsSerializer
    @authentication_classes([TokenAuthentication])
    def get_queryset(self):
        queryset = integrations.objects.all()
        limit = self.request.query_params.get('limit', None)
        offset = self.request.query_params.get('offset', None)
        level = self.request.query_params.get('level', None)
        role = self.request.COOKIES.get('role')
        userId = self.request.COOKIES.get('userId')

        if level is not None:
            queryset = queryset.filter(school_id_education_level_id_name_iexact = str(level))
        
        if limit is not None :
            if offset is None :
                queryset = queryset[:int(limit)] 
            else :
                queryset = queryset[int(offset):int(limit)]
        
        return queryset
     
    def list(self, request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        jumlahData = self.get_queryset().count()
        queryset = self.get_queryset()

        serializer = integrationsSerializer(queryset, many=True)
        response = {
            "data" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = integrationsSerializer(data = request.data)

        if serializer.is_valid(raise_exception= True):
            serializer.save()
            response = {
                "message" : "data integrasi baru telah ditambahkan",
                "data" : serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk = None):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = self.get_queryset()
        integrasi = get_object_or_404(queryset, pk=pk)
        serializer = integrationsSerializer(integrasi)
        response = {
            "message" : "detail instegrasi berhasil didapatkan",
            "data" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
     
     
    def update(self, request, pk = None):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = self.get_queryset()
        integrasi = get_object_or_404(queryset, pk=pk)
        serializer = integrationsSerializer(integrasi, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message" : "data integrasi berhasil diupdate"
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)