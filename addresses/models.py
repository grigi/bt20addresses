# Models for app 'addresses'
from django.db import models
import fields as map_fields

# Create your models here.

class Subject(models.Model):
    bttid = models.IntegerField(primary_key=True)
    
class Address(models.Model):
    subject = models.ForeignKey(Subject)
    date = models.DateField()
    
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
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)    