from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.institutions.models import institutions, institution_types
from apps.schools.models import schools, education_levels
from .modelsV2 import PersonInCharge, User, Role


def seed_superuser():
    superuser = get_user_model()
    if not User.objects.filter(email="admin@email.com").exists():
        superuser.objects.create_superuser(
            name="admin",
            email="admin@email.com",
            phone_number="+628144023168",
            password="123",
        )
        user = User.objects.get(email="admin@email.com")
        role = Role.objects.get(name="admin")
        user.role = role
        user.save()


def seed_user():
    users = [
        {
            "name": "John",
            "email": "john@email.com",
            "phone_number": "+6285867235034",
            "password": "123",
        },
        {
            "name": "Jane",
            "email": "jane@email.com",
            "phone_number": "+628300394259",
            "password": "123",
        },
    ]
    for user in users:
        User = get_user_model()
        if not User.objects.filter(email=user["email"]).exists():
            User.objects.create_user(
                name=user["name"],
                email=user["email"],
                phone_number=user["phone_number"],
                password=user["password"],
            )


def seed_role():
    roles = [
        {
            "name": "admin",
            "description": "Role Admin",
            "permissions": [
                {
                    "name": "user",
                    "actions": ["add", "change", "delete", "view"],
                    "model": User,
                },
                {
                    "name": "institutiontype",
                    "actions": ["add", "change", "delete", "view"],
                    "model": institution_types,
                },
                {
                    "name": "institution",
                    "actions": ["add", "change", "delete", "view"],
                    "model": institutions,
                },
                {
                    "name": "school",
                    "actions": ["add", "change", "delete", "view"],
                    "model": schools,
                },
                {
                    "name": "schoolcategory",
                    "actions": ["add", "change", "delete", "view"],
                    "model": education_levels,
                },
            ],
        },
        {
            "name": "penanggung_jawab_yayasan",
            "description": "Penanggung jawab yayasan",
            "permissions": [
                {
                    "name": "institutiontype",
                    "actions": ["view"],
                    "model": institution_types,
                },
                {
                    "name": "institution",
                    "actions": ["add", "view"],
                    "model": institutions,
                },
                {"name": "school", "actions": ["add", "view"], "model": schools},
                {
                    "name": "schoolcategory",
                    "actions": ["view"],
                    "model": education_levels,
                },
            ],
        },
        {
            "name": "penanggung_jawab_sekolah",
            "description": "Penanggung jawab sekolah",
            "permissions": [
                {
                    "name": "institutiontype",
                    "actions": ["view"],
                    "model": institution_types,
                },
                {
                    "name": "institution",
                    "actions": ["change", "view"],
                    "model": institutions,
                },
                {"name": "school", "actions": ["change", "view"], "model": schools},
                {
                    "name": "schoolcategory",
                    "actions": ["view"],
                    "model": education_levels,
                },
            ],
        },
    ]

    for role in roles:
        role_name = role["name"]
        description = role["description"]
        permissions = role["permissions"]

        # Create new role
        role, _ = Role.objects.get_or_create(name=role_name, description=description)

        for permission in permissions:
            perm_name = permission["name"]
            model = permission["model"]
            actions = permission["actions"]

            content_type = ContentType.objects.get_for_model(model)
            available_permissions = []
            # Check all available permissions for each roles
            for action in actions:
                codename = action + "_" + perm_name
                action_permitted = Permission.objects.get(
                    codename=codename, content_type=content_type
                )
                available_permissions.append(action_permitted)
            # Add all permissions to roles
            role.permissions.add(*available_permissions)


def seed_users_role_incharge():
    users = [
        {
            "email": "john@email.com",
            "role": "penanggung_jawab_sekolah",
            "institution_in_charge": "Sekolah-1",
        },
        {
            "email": "jane@email.com",
            "role": "penanggung_jawab_yayasan",
            "institution_in_charge": "Yayasan-0",
        },
    ]
    for user_data in users:
        user = User.objects.get(email=user_data["email"])
        role = Role.objects.get(name=user_data["role"])
        institution_in_charge = institutions.objects.get(
            name=user_data["institution_in_charge"]
        )
        # Adding role to user
        user.role = role
        user.save()
        # Adding Person In Charge (Penanggung Jawab)
        PersonInCharge.objects.get_or_create(
            user=user, institution=institution_in_charge
        )
