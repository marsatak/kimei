from django.core.management.base import BaseCommand
from accounts.models import sync_employees_with_personnel


class Command(BaseCommand):
    help = 'Synchronize Employees with Personnel data'

    def handle(self, *args, **options):
        sync_employees_with_personnel()
        self.stdout.write(self.style.SUCCESS('Successfully synchronized employees'))
