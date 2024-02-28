import random
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand
from employees.models import employees
from Account.models import employee_users

fake = Faker()

class Command(BaseCommand):
    help = 'Seed data user'

    def handle(self, *args, **kwargs):
        queryset = employees.objects.all()

        password = 'password'

        for pegawai in queryset:
            user = employee_users.objects.create(
                employee_id=pegawai,
                email=fake.email()
            )
            user.set_password(password)
            user.save()

            self.stdout.write(self.style.SUCCESS(f'berhasil melakukan seed'))