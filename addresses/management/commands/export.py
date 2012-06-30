from django.core.management.base import BaseCommand, CommandError
from addresses.models import *
import csv

class Command(BaseCommand):
    args = ''
    help = "Gets geometry data from Google"

    def handle(self, *args, **options):

        head = [
            'BTTID',
            'YEAR',
            'Number',
            'Road',
            'Suburb',
            'Area',
            'Province',
            'PostCode',
            'Migrated',
            'Latitude',
            'Longitude',
            'Google_Search_String',
            'Google_Latitude',
            'Google_Longitude',
            'Google_Street_Number',
            'Google_Route',
            'Google_Sublocality',
            'Google_Locality',
            'Google_City',
            'Google_Metro',
            'Google_Province',
            'Google_Country',
            'Google_Postcode',
            'Google_Type',
            'Google_Variance_KM',
            'Distance_KM',
        ]

        wr = csv.writer(open('/home/grigi/coding/bt20/gisreport.csv', 'wb'), quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(head)
        
        for addr in Address.objects.all():
            migrated = None
            if addr.migrated == True:
                migrated = 1
            if addr.migrated == False:
                migrated = 0
            variance = None
            try:
                variance = addr.gaccuracy/2.0
            except:
                pass
            val = [
                addr.subject.pk,
                addr.year,
                addr.number,
                addr.road,
                addr.suburb,
                addr.area,
                addr.province,
                addr.postcode,
                migrated,
                addr.lat,
                addr.lon,
                addr.address,
                addr.geolocation.lat,
                addr.geolocation.lon,
                addr.gstreet,
                addr.groute,
                addr.gsublocality,
                addr.glocality,
                addr.gcity,
                addr.gmetro,
                addr.gprovince,
                addr.gcountry,
                addr.gpostcode,
                addr.gtype,
                variance,
                addr.distance,
            ]
            wr.writerow([s.encode('utf8') if type(s) is unicode else s for s in val])

            
