from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from apps.employees.models import employees
from apps.institutions.models import pic_institutions

# Create your models here.
def upload(instance, filename):
    ext = filename.split('.')[-1]
    return 'media/employees/{}'.format(filename)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_yayasan(self,email,password=None,**extra_fileds):
        queryset = pic_users.objects.all()
        user = queryset.model(email, **extra_fileds)
        user.is_yayasan = True
        user.set_password(password)
        user.save(useing=self._db)

    def create_superuser(self, email,password=None,**extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)
    
class CostumUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255,null=False)
    email = models.CharField(max_length=100, null=False, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_yayasan = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['password']

    
class pic_users(CostumUser):
    pic_id = models.ForeignKey(pic_institutions, on_delete=models.CASCADE, null=False)
    email_verified_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table='pic_users'

class pic_user_data_changes(models.Model):
    id = models.AutoField(primary_key=True)
    pic_user_id = models.ForeignKey(CostumUser, on_delete=models.CASCADE, null=False)
    pic_id = models.BigIntegerField(max_length=20, null=False)
    password = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=100, null=False, db_index=True, unique=True)
    email_verified_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='pic_user_data_changes'

class log_pic_users(models.Model):
    id = models.AutoField(primary_key=True)
    pic_id = models.ForeignKey(CostumUser, on_delete=models.CASCADE, null=False)
    action_choices = [
        ("1", "Login"),
        ("2", "Logout")
    ]
    action = models.CharField(max_length=1, null=False, choices=action_choices)
    last_ip_address = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,)

    class Meta:
        db_table = 'log_pic_users'

class employee_users(CostumUser):
    # id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(employees,on_delete= models.CASCADE, null=True)
    # email = models.CharField(max_length=100, null=False, db_index=True, unique=True)
    # password = models.CharField(max_length=255,null=False)
    email_verified_at = models.DateTimeField(null=True,blank=True, default=None)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # deleted_at = models.DateTimeField(null=True, blank=True)

    # is_staff = models.BooleanField(default=False)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['password']

    # objects = UserManager()
    
    # @staticmethod
    # def has_perm(perm, obj=None):
    #     return True
    # @staticmethod
    # def has_module_perms(app_label):
    #     return True
    # @property
    # def is_staff(self):
    #     return self.is_staff

    class Meta:
        db_table = 'employee_users'

class employee_user_data_changes(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CostumUser, on_delete=models.CASCADE)
    employee_id = models.BigIntegerField(max_length=20, db_index=True)
    email = models.CharField(max_length=100, null=False, db_index=True, unique=True)
    password = models.CharField(max_length=255,null=False)
    email_verified_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employee_user_data_changes'

class log_employee_users(models.Model):
    id = models.AutoField(primary_key=True)
    employee_user_id = models.ForeignKey(CostumUser, on_delete=models.CASCADE)
    action_choices = [
        ("1", "Login"),
        ("2", "Logout")
    ]
    action = models.CharField(max_length=1, null=False, choices=action_choices)
    last_ip_address = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'log_employee_users'