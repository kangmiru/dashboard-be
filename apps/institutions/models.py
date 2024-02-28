from django.db import models
from datetime import datetime
from apps.employees.models import employees
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
def upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ext)
    return 'media/institutions/{}'.format(filename)

class villages(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'villages'

class institution_types(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=False,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'instituition_types'

class institutions(models.Model):
    id = models.AutoField(primary_key=True)
    institution_type_id = models.ForeignKey(institution_types, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=False)
    leader_name = models.CharField(max_length=255, null=True)
    address = models.TextField(null=False)
    email = models.CharField(max_length=100, null=True, db_index=True, unique=True, blank=False)
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    logo = models.ImageField(null=True, blank=True, upload_to=upload)
    status_choices = [
        ("1", "active"),
        ("2", "suspended"),
        ("3", "inactive")
    ]
    status = models.CharField(max_length=1, null=False, default="1", choices= status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'institutions'

class institution_data_changes(models.Model):
    id = models.AutoField(primary_key=True)
    institution_id = models.ForeignKey(institutions, on_delete=models.CASCADE)
    institution_type_id = models.BigIntegerField(max_length=20,null=False)
    leader_name = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255,null=False)
    address = models.TextField(null=False)
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    logo = models.TextField(null=True, blank=True)
    status_choices = [
        ("1", "active"),
        ("2", "suspended"),
        ("3", "inactive")
    ]
    status = models.CharField(max_length=1, null=False, default="1", choices= status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta :
        db_table = 'institution_data_changes'

class pic_institutions(models.Model):
    id = models.AutoField(primary_key=True)
    institution_id = models.ForeignKey(institutions, on_delete=models.CASCADE)
    nik = models.CharField(max_length=16, null=True, db_index=True, unique=True)
    name = models.CharField(max_length=255, null=True)
    gender_choices = [
        ("1", "male"),
        ("2", "female")
    ]
    gender = models.CharField(max_length=1, default="1", null=True, db_index=True,choices=gender_choices)
    date_of_birth = models.DateField(null=True, db_index=True)
    village_id = models.ForeignKey(villages, on_delete=models.CASCADE, db_index=True)
    address = models.TextField(null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    display_photo =models.ImageField(null=True, blank=True, upload_to=upload)
    photo_identity_number = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'pic_institutions'

class pic_institution_data_changes(models.Model):
    id = models.AutoField(primary_key=True)
    pic_id = models.ForeignKey(pic_institutions, on_delete=models.CASCADE, null=True)
    institution_id = models.BigIntegerField(max_length=20, null=True)
    nik = models.CharField(max_length=16, null=True)
    name = models.CharField(max_length=255,null=True)
    gender_choices = [
        ("1", "male"),
        ("2", "female")
    ]
    gender = models.CharField(max_length=1, default="1", null=True, db_index=True,choices=gender_choices)
    date_of_birth = models.DateField(null=True, db_index=True)
    village_id = models.ForeignKey(villages, on_delete=models.CASCADE, db_index=True)
    address = models.TextField(null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    display_photo = models.ImageField(null=True, default=None)
    photo_identity_number = models.ImageField(null=True, default=None, upload_to=upload)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table='pic_institution_data_changes'

class institution_verifications(models.Model):
    id = models.UUIDField(primary_key=True, null=False)
    institution_id = models.ForeignKey(institutions, on_delete=models.CASCADE, null=False)
    verified_by = models.ForeignKey(employees, on_delete=models.CASCADE, null=False)
    status_choices = [
        ("1", "pending"),
        ("2", "accepted"),
        ("3", "rejected")
    ]
    status = models.CharField(max_length=1, null=False, default="1",choices=status_choices, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='institution_verification'