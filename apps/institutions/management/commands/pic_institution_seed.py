import random
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand
from institutions.models import institutions, pic_institutions, villages

fake = Faker()

class Command(BaseCommand):
    help = 'Seed data institusi'

    def handle(self, *args, **kwargs):
        queryset = institutions.objects.all()

        for institution in queryset:
            ins = pic_institutions.objects.create(
                institution_id = institution,
                nik = fake.random_int(min=1000000, max=9999999),
                name = fake.name(),
                gender = fake.random_element(elements=('1','2')),
                date_of_birth = fake.date_of_birth(),
                village_id = fake.random_element(elements=villages.objects.all()),
                address =fake.city(),
                phone_number = fake.random_int(min=100000, max=999999)
            )

            self.stdout.write(self.style.SUCCESS(f'berhasil melakukan seed'))