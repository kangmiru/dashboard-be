from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('',schoolView.as_view({'get':'list','post':'create'}), name="sekolah"),
    path('<int:pk>/',schoolView.as_view({'get':'retrieve','put':'update','delete':'destroy'}), name="sekolah"),
    path('education_levels/', EducationLevelsView.as_view({'get':'list', 'post':'create'}), name="EducationLevels"),
]