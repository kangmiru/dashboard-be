from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
def upload(instance, filename):
    ext = filename.split('.')[-1]
    return 'media/employees/{}'.format(filename)

class employees(models.Model):
    id = models.AutoField(primary_key=True)
    nik = models.CharField(max_length=16, null=False, db_index=True)
    name = models.CharField(max_length=255, null=False)
    display_photo = models.ImageField(null=True, blank=True, upload_to='asset/employees/')
    status_choices = [
        ("1", "active"),
        ("2", "suspended"),
        ("3", "inactive")
    ]
    status = models.CharField(max_length=1, null=False, default="1", choices= status_choices ,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'employees'

class employee_data_changes(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(employees,on_delete= models.CASCADE)
    nik = models.CharField(max_length=16, null=False, db_index=True)
    name = models.CharField(max_length=255,null=False)
    display_photo = models.TextField(null=True, default=None)
    status_choices = [
        ("1", "active"),
        ("2", "suspended"),
        ("3", "inactive")
    ]
    status = models.CharField(max_length=1, null=False, default="1", choices= status_choices ,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'employee_data_changes'

