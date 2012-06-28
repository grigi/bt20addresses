from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
import csv

from addresses.models import *

cols = []
datarow = []
map = None

def intnone(v):
    if v is None:
        return None
    return int(v)

def floatnone(v):
    if v is None or v == '':
        return None
    return float(v)

def setnotnone(o,a,v):
    if v is not None and str(v) != '':
        setattr(o,a,v)
        return 1
    return 0

def var(s):
    i = 0
    index = None
    for n in cols:
        if s == n:
            index = i
        i += 1
    
    if index is not None:
        return str(datarow[index])
    else:
        return None

def province(s):
    p = var(s)
    if p is None:
        return None
    if p.lower() == 'gp':
        p = 'Gauteng'
    return p

datafolder = '%s/data/' % (settings.PROJECT_ROOT)

dataorder = [
    # Addresses
    #'yr14 bt20 addresses and migration codes 24 march 2009.csv',
    #'yr18 migration updated feb 09 2012.csv',
    # GPS Data
    #'Year 13 Mobile Adol Section 1 GPS Coordinates.csv',
    
    # Validated Data
    '3273 homes of non-movers Nov 4 2011.csv',
]

datamap = {
    '3273 homes of non-movers Nov 4 2011.csv': [
        {
            'bttid': (var, 'bttid'),
            'year': (None, 1996),
            'number': (var, 'homenumber'),
            'road': (var, 'homeroad'),
            'suburb': (var, 'homesuburb'),
            'area': (var, 'homearea'),
            'province': (province, 'homeprov'),
            'lat': (var, 'home_lat'),
            'lon': (var, 'home_long'),
        },
        {
            'bttid': (var, 'bttid'),
            'year': (None, 1997),
            'number': (var, 'homenumber'),
            'road': (var, 'homeroad'),
            'suburb': (var, 'homesuburb'),
            'area': (var, 'homearea'),
            'province': (province, 'homeprov'),
            'lat': (var, 'home_lat'),
            'lon': (var, 'home_long'),
        },
        {
            'bttid': (var, 'bttid'),
            'year': (None, 1998),
            'number': (var, 'homenumber'),
            'road': (var, 'homeroad'),
            'suburb': (var, 'homesuburb'),
            'area': (var, 'homearea'),
            'province': (province, 'homeprov'),
            'lat': (var, 'home_lat'),
            'lon': (var, 'home_long'),
        },
        {
            'bttid': (var, 'bttid'),
            'year': (None, 1999),
            'number': (var, 'homenumber'),
            'road': (var, 'homeroad'),
            'suburb': (var, 'homesuburb'),
            'area': (var, 'homearea'),
            'province': (province, 'homeprov'),
            'lat': (var, 'home_lat'),
            'lon': (var, 'home_long'),
        },
        {
            'bttid': (var, 'bttid'),
            'year': (None, 2000),
            'number': (var, 'homenumber'),
            'road': (var, 'homeroad'),
            'suburb': (var, 'homesuburb'),
            'area': (var, 'homearea'),
            'province': (province, 'homeprov'),
            'lat': (var, 'home_lat'),
            'lon': (var, 'home_long'),
        },
        {
            'bttid': (var, 'bttid'),
            'year': (None, 2001),
            'number': (var, 'homenumber'),
            'road': (var, 'homeroad'),
            'suburb': (var, 'homesuburb'),
            'area': (var, 'homearea'),
            'province': (province, 'homeprov'),
            'lat': (var, 'home_lat'),
            'lon': (var, 'home_long'),
        },
        {
            'bttid': (var, 'bttid'),
            'year': (None, 2002),
            'number': (var, 'homenumber'),
            'road': (var, 'homeroad'),
            'suburb': (var, 'homesuburb'),
            'area': (var, 'homearea'),
            'province': (province, 'homeprov'),
            'lat': (var, 'home_lat'),
            'lon': (var, 'home_long'),
        },
        {
            'bttid': (var, 'bttid'),
            'year': (None, 2003),
            'number': (var, 'homenumber'),
            'road': (var, 'homeroad'),
            'suburb': (var, 'homesuburb'),
            'area': (var, 'homearea'),
            'province': (province, 'homeprov'),
            'lat': (var, 'home_lat'),
            'lon': (var, 'home_long'),
        },
    ]
}

def get(attr):
    (fun, val) = map[attr]
    if fun is None:
        return val
    else:
        return fun(val)

class Command(BaseCommand):
    args = ''
    help = "Imports the bt20 CSVs"

    def handle(self, *args, **options):
        global cols
        global datarow
        global map
        
        transaction.enter_transaction_management(managed=True)
        transaction.managed(flag=True)
        
        for filename in dataorder:
            for map in datamap[filename]:
                print "Importing '%s' - %s" % (filename, map['year'][1])
            
                rdr = csv.reader(open(datafolder + filename, 'rb'))
                
                cols = rdr.next()
                #print ', '.join(cols)
                
                naddr = 0
                uaddr = 0
                saddr = 0
                
                for datarow in rdr:
                    try:
                        subject = Subject.models.get(bttid=intnone(get('bttid')))
                    except:
                        subject = Subject(bttid=intnone(get('bttid')))
                        subject.save()
    
                    try:
                        addr = Address.models.get(subject=subject, year=intnone(get('year')))
                        uaddr += 1
                    except:
                        addr = Address(
                            subject=subject,
                            year=intnone(get('year')),
                        )
                        naddr += 1
                    
                    cnt = 0                 
                    cnt += setnotnone(addr,'number',get('number'))
                    cnt += setnotnone(addr,'road',get('road'))
                    cnt += setnotnone(addr,'suburb',get('suburb'))
                    cnt += setnotnone(addr,'area',get('area'))
                    cnt += setnotnone(addr,'province',get('province'))
                    cnt += setnotnone(addr,'lat',floatnone(get('lat')))
                    cnt += setnotnone(addr,'long',floatnone(get('lon')))
                    
                    if cnt == 0:
                        saddr += 1

                    addr.save()
                    
                    if ((naddr+uaddr) % 1000) == 0:
                        transaction.commit()
                 
                transaction.commit()
                print '%d New, %d Updated, %d Empty' % (naddr, uaddr, saddr)
            
