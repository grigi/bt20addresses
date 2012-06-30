from django.core.management.base import BaseCommand, CommandError
from addresses.models import *
import sys

class Command(BaseCommand):
    args = ''
    help = "Gets geometry data from Google"

    def handle(self, *args, **options):
        
        for addr in Address.objects.filter(address__isnull=False, gtype__isnull=True).order_by('pk'):
            print addr.pk, addr
            addr.getgeo()
            #sys.stdout.write('.')
            #sys.stdout.flush()
        
        print ""

            
