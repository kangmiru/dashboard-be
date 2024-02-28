import random
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand
from institutions.models import pic_institutions
from Account.models import pic_users

fake = Faker()

class Command(BaseCommand):
    help = 'Seed data user'

    def handle(self, *args, **kwargs):
        queryset = pic_users.objects.all()

        password = 'password'

        for pegawai in queryset:
            user = pic_users.objects.create(
                pic_id=pegawai,
                email=fake.email()
            )
            user.set_password(password)
            user.save()

            self.stdout.write(self.style.SUCCESS(f'berhasil melakukan seed'))