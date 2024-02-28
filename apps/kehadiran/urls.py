from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('kehadiran/karyawan', KehadiranView.as_view({'get':'get_kehadiran_karyawan'}), name="kehadiran-karyawan")
]