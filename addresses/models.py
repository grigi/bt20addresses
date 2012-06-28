# Models for app 'addresses'
from django.db import models
import fields as map_fields
import re
import math

# Create your models here.

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
    
    # Provided GPS coords
    olat = models.FloatField(null=True, blank=True) 
    olong = models.FloatField(null=True, blank=True)
    
    # Generated addr data
    address = map_fields.AddressField(max_length=200, null=True, blank=True)
    geolocation = map_fields.GeoLocationField(max_length=100, null=True, blank=True)
    
    # Verify distance in KM
    distance = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.address is None or self.address == '':
            # suburb extention stuff tends to confuse google
            suburb = re.sub(r' [Ee][Xx][Tt] .*', r'', self.suburb)
            address = '%s %s, %s, %s, %s, South Africa' % (self.number, self.road, suburb, self.area, self.province)
            self.address = re.sub(r',\s*,', r',', address)
        if self.olat is not None and self.olong is not None and (self.geolocation is not None or self.geolocation != ''):
            # Compute approx distance, where 1 arc-hour is 108km
            nlat = self.geolocation.lat
            nlong = self.geolocation.lon
            self.distance = math.sqrt(math.pow((self.olat - nlat),2) + math.pow((self.olong - nlong),2)) * 108.0
            print '%.5f, %.5f to %.5f, %.5f = %.3f km' % (self.olat, self.olong, nlat, nlong, self.distance) 
        super(Address, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s - %s' % (self.subject, self.year)
        
    class Meta:
        unique_together = (("subject", "year"),)