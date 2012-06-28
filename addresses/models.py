# Models for app 'addresses'
from django.db import models
import fields as map_fields
import re
import math
from pygeocoder import Geocoder

# Create your models here.

def bos(s):
    if s is None:
        return ''
    return s

class Subject(models.Model):
    bttid = models.IntegerField(primary_key=True)

    def __unicode__(self):
        return '%d' % (self.bttid)
    
class Address(models.Model):
    subject = models.ForeignKey(Subject)
    year = models.IntegerField()
    
    # Address
    number = models.CharField(max_length=255, null=True, blank=True)
    road = models.CharField(max_length=255, null=True, blank=True)
    suburb = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    changed = models.NullBooleanField(null=True, blank=True)
    
    # Provided GPS coords
    lat = models.FloatField(null=True, blank=True) 
    lon = models.FloatField(null=True, blank=True)
    
    # Generated addr data
    address = map_fields.AddressField(max_length=200, null=True, blank=True)
    
    # Google returned results
    geolocation = map_fields.GeoLocationField('Estimated Location',max_length=100, null=True, blank=True)
    gstreet = models.CharField(max_length=255, null=True, blank=True)
    groute = models.CharField(max_length=255, null=True, blank=True)
    gsublocality = models.CharField(max_length=255, null=True, blank=True)
    glocality = models.CharField(max_length=255, null=True, blank=True)
    gcity = models.CharField(max_length=255, null=True, blank=True)
    gmetro = models.CharField(max_length=255, null=True, blank=True)
    gprovince = models.CharField(max_length=255, null=True, blank=True)
    gcountry = models.CharField(max_length=255, null=True, blank=True)
    gpostcode = models.CharField(max_length=255, null=True, blank=True)
    gtype = models.CharField(max_length=255, null=True, blank=True)
    gaccuracy = models.FloatField('Variance KM', null=True, blank=True)
    
    # Stats on the data validity
    distance = models.FloatField('Distance KM', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.wash()

        if self.lat is not None and self.lon is not None:
            # Compute approx distance, where 1 arc-hour is 108km
            nlat = self.geolocation.lat
            nlon = self.geolocation.lon
            if nlat is not None and nlon is not None:
                self.distance = math.sqrt(math.pow((self.lat - nlat),2) + math.pow((self.lon - nlon),2)) * 108.0
                print '%.5f, %.5f to %.5f, %.5f = %.3f km' % (self.lat, self.lon, nlat, nlon, self.distance) 
        
        super(Address, self).save(*args, **kwargs)

    def wash(self):
        if self.address == '':
            self.address = None
            
        if self.road == '98' or self.road == '99':
            self.road = None

        if self.suburb == '98' or self.suburb == '99':
            self.suburb = None

        if self.area == '98' or self.area == '99':
            self.area = None

        if self.province == '98' or self.province == '99':
            self.province = None
        
        if self.road is None and self.suburb is None and self.area is None:
            if self.number == '98' or self.number == '99':
                self.number = None
                
        if self.address is None:
            # suburb extention stuff tends to confuse google
            if self.suburb is None:
                suburb=''
            else:
                suburb = re.sub(r' [Ee][Xx][Tt] .*', r'', self.suburb)
                suburb = re.sub(r' [Zz][Oo][Nn][Ee] .*', r'', suburb)
                suburb = re.sub(r' [Bb][Ll][Oo][Cc][Kk] .*', r'', suburb)
            address = '%s %s, %s, %s, %s, South Africa' % (bos(self.number), bos(self.road), suburb, bos(self.area), bos(self.province))
            self.address = re.sub(r',\s*,', r',', address)
            if len(self.address) < 20:
                self.address = None
            
            # At this point all the google collected data is invalid (if it even has been done yet)
            self.gstreet = None
            self.groute = None
            self.gsublocality = None
            self.glocality = None
            self.gcity = None
            self.gmetro = None
            self.gprovince = None
            self.gcountry = None
            self.gpostcode = None
            self.gtype = None
            self.gaccuracy = None
            
    
    def getgeo(self):
        if self.address is not None and self.gtype is None:
            results = Geocoder.geocode(self.address)
            if len(results) > 0:
                print self.address
                (self.geolocation.lat, self.geolocation.lon) = results[0].coordinates
                self.gstreet = results[0].street_number
                self.groute = results[0].route
                self.gsublocality = results[0].sublocality
                self.glocality = results[0].locality
                self.gcity = results[0].administrative_area_level_3
                self.gmetro = results[0].administrative_area_level_2
                self.gprovince = results[0].administrative_area_level_1
                self.gcountry = results[0].country
                self.gpostcode = results[0].postal_code
                self.gtype = results[0].raw[0]['geometry']['location_type']
                try:
                    bounds = results[0].raw[0]['geometry']['bounds']
                    self.gaccuracy = math.sqrt(math.pow((bounds['northeast']['lat'] - bounds['southwest']['lat']),2) + math.pow((bounds['northeast']['lng'] - bounds['southwest']['lng']),2)) * 108.0
                except:
                    self.gaccuracy = None
                    
            self.save()
            
    
    def __unicode__(self):
        return '%s - %s' % (self.subject, self.year)
        
    class Meta:
        unique_together = (("subject", "year"),)