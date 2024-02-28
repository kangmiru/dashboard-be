# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as User_Admin

# from .forms import UserCreationForm, UserChangeForm
# from .modelsV2 import User, Role, PersonInCharge


# class UserAdmin(User_Admin):
#     add_form = UserCreationForm
#     form = UserChangeForm
#     model = User
#     list_display = ("email", "name", "is_staff", "is_active", "created_at")
#     list_filter = ("email", "name", "is_staff", "is_active", "created_at")
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (
#             "Permissions",
#             {"fields": ("is_staff", "is_active", "role", "user_permissions")},
#         ),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "email",
#                     "name",
#                     "password1",
#                     "password2",
#                     "is_staff",
#                     "is_active",
#                     "role",
#                     "user_permissions",
#                 ),
#             },
#         ),
#     )
#     search_fields = ("email",)
#     ordering = ("email",)


# class PICManager(admin.ModelAdmin):
#     list_display = ["user", "institution", "created_at"]


# admin.site.register(User, UserAdmin)
# admin.site.register(Role)
# admin.site.register(PersonInCharge, PICManager)