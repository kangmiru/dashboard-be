from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes

from apps.institutions.models import pic_institution_data_changes

from .serializers import (
    educationLevelsSerializer,
    schoolsSerializer
)

from .models import (
    schools,
    education_levels
)

from apps.Account.models import *

class EducationLevelsView(viewsets.ModelViewSet):
    serializer_class = educationLevelsSerializer
    @authentication_classes([TokenAuthentication])

    def get_queryset(self):
        return education_levels.objects.all()
    
    def list(self, request):
        if not request.user.is_staff:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = self.get_queryset()
        serializer = educationLevelsSerializer(queryset, many=True)

        data = serializer.data

        return Response({'data':data}, status=status.HTTP_200_OK)
    
    def create(self, request):
        if request.user.is_staff:
            serializer = educationLevelsSerializer(data = request.data)

            if serializer.is_valid(raise_exception= True):
                serializer.save()
                response = {
                    "message" : "data education level telah ditambahkan",
                    "data" : serializer.data
                }

                return Response(response, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
    
class schoolView(viewsets.ModelViewSet):
    serializer_class = schoolsSerializer
    @authentication_classes([TokenAuthentication])

    def get_queryset(self):
        queryset = schools.objects.all()
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
            serializer = schoolsSerializer(queryset, many=True)
            response = {
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def create(self, request):
        if request.user.is_staff:
            serializer = schoolsSerializer(data = request.data)

            if serializer.is_valid(raise_exception= True):
                serializer.save()
                response = {
                    "message" : "data sekolah baru telah ditambahkan",
                    "data" : serializer.data
                }

                return Response(response, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def retrieve(self, request, pk = None):
        if request.user.is_staff:
            queryset = schools.objects.all()
            institution = get_object_or_404(queryset, pk=pk)
            serializer = schoolsSerializer(institution)
            response = {
                "message" : "detail sekolah",
                "data" : serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'message':'anda tidak hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def update(self, request, pk = None):
        if request.user.is_staff:
            queryset = schools.objects.all()
            institution = get_object_or_404(queryset, pk=pk)
            serializer = schoolsSerializer(institution, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message':'data berhasil diubah'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'message':'anda tidak memiliki hak akses'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def destroy(self, request, pk = None):
        if request.user.is_staff:
            queryset = schools.objects.all()
            institusi = get_object_or_404(queryset, pk=pk)
            serializer = schoolsSerializer(institusi)

            institusi.delete()

            return Response({'message':'data berhasil dihapus'}, status=status.HTTP_200_OK)
        
        else:
            return Response({'message':'anda tidak memilik hak akses'}, status=status.HTTP_401_UNAUTHORIZED)