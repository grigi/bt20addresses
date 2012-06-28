# Admin for app 'addresses'
from django.contrib import admin
from models import *
import widgets as map_widgets
import fields as map_fields

# Create your admin config here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ['subject', 'year', 'address', 'oloc', 'geolocation', 'distance']
    formfield_overrides = {
       map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},    
    }
    
    def oloc(self, obj):
        try:
            return '%.5f, %.5f' % (obj.olat, obj.olong)
        except:
            return ''
    oloc.short_description='Recorded location'
    
admin.site.register(Address, AddressAdmin)

class AddressInline(admin.TabularInline):
    readonly_fields = ['address', 'geolocation', 'distance']
    model = Address
    extra = 0
class SubjectAdmin(admin.ModelAdmin):
    inlines=[AddressInline]
admin.site.register(Subject, SubjectAdmin)
