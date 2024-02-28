import random
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand
from institutions.models import institutions, institution_types

fake = Faker()

class Command(BaseCommand):
    help = 'Seed data institutsi'

    def handle(self, *args, **kwargs):
        queryset = institution_types.objects.all()

        for institution in queryset:
            ins = institutions.objects.create(
                institution_type_id = institution,
                name = fake.name(), # nama yayasan
                leader_name = fake.name(),
                address = fake.city(),
                email = fake.email(),
                phone_number = fake.random_int(min=10000000, max=99999999),
                status = fake.random_element(elements=('1','2','3'))
            )

            self.stdout.write(self.style.SUCCESS(f'berhasil melakukan seed'))