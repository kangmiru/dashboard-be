import random
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand
from employees.models import employees

fake = Faker()

# melacak nomor yang dihasilkan
generate_number = set()

def generate_unique_number(digits):
    while True:
        random_number = fake.random_number(digits=digits)
        if random_number not in generate_number:
            generate_number.add(random_number)
            return random_number

random_number_16_digits = generate_unique_number(digits=16)

class Command(BaseCommand):
    help = 'Seed data untuk employee'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('seeding data... '))

        num_empolyee = 10

        for _ in range(num_empolyee):
            employees.objects.create(
                nik = random_number_16_digits,
                name = fake.name(),
                status = fake.random_element(elements=('1','2','3')),
            )

        self.stdout.write(self.style.SUCCESS(f'sukses melakukan seed employee'))