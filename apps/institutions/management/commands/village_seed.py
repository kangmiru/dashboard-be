from typing import Any
from django.core.management.base import BaseCommand
from institutions.models import villages
from faker import Faker

faker = Faker()

class Command(BaseCommand):
    help = 'Seed data to database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('seeding data'))

        num_village = 5

        for _ in range(num_village):
            villages.objects.create(
                name = faker.name(),
            )

        self.stdout.write(self.style.SUCCESS(f'sukses melakukan seed'))