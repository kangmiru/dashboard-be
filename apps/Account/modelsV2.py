# from django.db import models
# from django.contrib.auth.models import AbstractUser, Permission
# from django.utils.translation import gettext_lazy as _
# from phonenumber_field.modelfields import PhoneNumberField

# from .manager import UserManager


# class Role(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     permissions = models.ManyToManyField(Permission, related_name="permissions")
#     description = models.CharField(_("Description"), max_length=200, blank=True)

#     def __str__(self):
#         return self.name


# class User(AbstractUser):
#     username = None
#     name = models.CharField(_("Nama lengkap"), max_length=50)
#     email = models.EmailField(_("Email"), max_length=254, unique=True)
#     phone_number = PhoneNumberField(_("Nomor telepon"))
#     role = models.ForeignKey(
#         Role,
#         verbose_name=_("roles"),
#         blank=True,
#         null=True,
#         help_text="The roles belong to User for authorization permission",
#         related_name="role",
#         on_delete=models.SET_NULL,
#     )
#     image = models.ImageField(null=True, upload_to="images/institutions")
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["name", "phone_number", "name", "phone_number", "role"]

#     objects = UserManager()

#     def __str__(self):
#         return self.email


# class PersonInCharge(models.Model):
#     user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
#     institution = models.ForeignKey(
#         "institution.Institution",
#         verbose_name=_("Instansi"),
#         on_delete=models.CASCADE,
#     )
#     created_at = models.DateTimeField(auto_now_add=True, null=True)

#     REQUIRED_FIELDS = ["user", "institution"]

#     def __str__(self):
#         return self.user.name
