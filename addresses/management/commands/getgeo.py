from django.core.management.base import BaseCommand, CommandError
from addresses.models import *

class Command(BaseCommand):
    args = ''
    help = "Gets geometry data from Google"

    def handle(self, *args, **options):
        
        for addr in Address.objects.filter(address__isnull=False, gtype__isnull=True):
            addr.getgeo()
            
