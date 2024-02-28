from django.core.management.base import BaseCommand
from institutions.models import institution_types

class Command(BaseCommand):
    help = 'Seed data to the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('seeding data... '))
        
        data_seed = [
            {'name': 'Yayasan'},
            {'name': 'Sekolah'},
        ]

        # Tambahkan data seed ke model
        for item in data_seed:
            institution_types.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('Data seed berhasil ditambahkan'))