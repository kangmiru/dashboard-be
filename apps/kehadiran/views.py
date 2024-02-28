from django.shortcuts import render
from rest_framework import viewsets
import requests

from apps.integrations.models import integrations
from apps.schools.models import schools

class KehadiranView(viewsets.ViewSet):

    def get_kehadiran_karyawan(self, request, name=None):
        try:
            queryset = schools.objects.all().order_by('created_at')
            school_object = queryset.get(name='demo SMK')  # Ubah sesuai dengan nama model dan nama field yang sesuai

            api_url = school_object.dns  # Pastikan ada atribut dns di model schools

            response = requests.get(f'{api_url}/api/karyawan/presence/monthly')

            if response.status_code == 200:
                data = response.json()
                # Proses data yang diterima
                return render(request, 'api_data.html', {'data': data})
            else:
                return render(request, 'api_error.html')
        except schools.DoesNotExist:
            return render(request, 'api_error.html', {'error_message': 'School not found'})