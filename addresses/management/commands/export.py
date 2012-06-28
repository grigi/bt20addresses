from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = ''
    help = "Export a report in CSV format"

    def handle(self, *args, **options):
        pass
