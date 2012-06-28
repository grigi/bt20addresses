# Admin for app 'addresses'
from django.contrib import admi
from models import *
import widgets as map_widgets
import fields as map_fields

# Create your admin config here.

class AddressAdmin(admin.ModelAdmin):
    formfield_overrides = {
       map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},    
    }
admin.site.register(Address, AddressAdmin)

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
class SubjectAdmin(admin.ModelAdmin):
    inlines=[AddressInline]
admin.site.register(Subject, SubjectAdmin)
