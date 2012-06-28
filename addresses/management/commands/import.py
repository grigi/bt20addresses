from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = ''
    help = "Imports the bt20 CSVs"

    def handle(self, *args, **options):
        pass
