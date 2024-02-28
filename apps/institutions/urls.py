from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    # institusi
    path('', InstitutionViews.as_view({'get':'list_total'}), name="Institutions"),
    path('list/', InstitutionViews.as_view({'get':'list', 'post':'create'}), name="Institutions"),
    path('list/<int:pk>/', InstitutionViews.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'}), name="institutionRetrieveUpdateDestroy"),
    path('pic/', picInstitutionsView.as_view({'get':'list','post':'create'}), name="PicInstitution"),
    path('pic/<int:pk>/', picInstitutionsView.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'}), name="PicInstitutionRetrieveUpdateDestroy"),
    path('yayasan/', InstitutionViews.as_view({'get':'list_yayasan'}), name="yayasan"),
    path('sekolah/', InstitutionViews.as_view({'get':'list_sekolah'}), name="sekolah"),
    
    # developer
    path('type/', institutionTypeViews.as_view({'get':'list', 'post':'create'}), name="InstitutionTypes"),

    # user
    path('pic/users/', picUserView.as_view({'get':'list', 'post':'create'}), name="PicUSer"),
    path('pic/statistics', picLoginStatisticsView.as_view({'get':'list'}), name="PicLoginStatistics")
]

# pic = penanggung jawab