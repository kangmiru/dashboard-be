from django.core.management.base import BaseCommand
from schools.models import education_levels

class Command(BaseCommand):
    help = 'Seed data to the database'

    def handle(self, *args, **options):
        data_seed = [
            {'name': 'TK'},
            {'name': 'SD'},
            {'name': 'SMP'},
            {'name': 'SMA'},
        ]

        # Tambahkan data seed ke model
        for item in data_seed:
            education_levels.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('Data seed berhasil ditambahkan'))