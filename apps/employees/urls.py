from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('', EmployeesView.as_view({'get':'list', 'post':'create'}), name="employees"),
    path('admin/', EmployeeUserView.as_view({'get':'list','post':'create'}), name="employeeUsers"),
]