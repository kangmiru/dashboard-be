from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('', institutionSchoolView.as_view({'get':'list', 'post':'create'}) , name="integrations"),
    path('yayasan/<int:pk>/', institutionSchoolView.as_view({'get':'view_yayasan'}) , name="integrations-yayasan"),
    path('yayasan/<int:pk>/<slug:name>/', institutionSchoolView.as_view({'get':'view_sekolah'}) , name="integrations-sekolah"),
    path('<int:pk>/', institutionSchoolView.as_view({'get':'retrieve', 'put':'update'}) , name="integrations-detail"),
    path('schools/', integrationView.as_view({'get':'list','post':'create'}), name="institutionSchool"),
    path('schools/<int:pk>', integrationView.as_view({'get':'retrieve', 'put':'update'}), name=" institutionSchRetrieveUpdate"),
    path('verification/', institutionSchoolVerView.as_view({'get':'list', 'post':'create'}), name="institutionSchoolVer"),
    path('verification/<int:pk>', institutionSchoolVerView.as_view({'get':'retrieve','put':'update'}), name="institutionSchVerRetrieveUpdate"),
]