from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('login/', EmployeeLoginView.as_view({'post':'login'}), name="employeeLogin"),
    path('logout/', EmployeeLogoutView.as_view({'post':'logout'}), name="employeeLogout"),
]