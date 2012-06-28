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
    '3273 homes of non-movers Nov 4 2011.csv',
]

datamap = {
    '3273 homes of non-movers Nov 4 2011.csv': {
        'bttid': (var, 'bttid'),
        'year': (None, 1990),
        'number': (var, 'homenumber'),
        'road': (var, 'homeroad'),
        'suburb': (var, 'homesuburb'),
        'area': (var, 'homearea'),
        'province': (province, 'homeprov'),
        'lat': (var, 'home_lat'),
        'lon': (var, 'home_long'),
    }
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
            print "Importing '%s'" % (filename)
            
            map = datamap[filename]
            
            rdr = csv.reader(open(datafolder + filename, 'rb'))
            
            cols = rdr.next()
            #print ', '.join(cols)
            
            naddr = 0
            uaddr = 0
            
            for datarow in rdr:
                try:
                    subject = Subject.models.get(bttid=intnone(get('bttid')))
                    uaddr += 1
                except:
                    subject = Subject(bttid=intnone(get('bttid')))
                    subject.save()
                    naddr += 1
                
                addr = Address(
                    subject=subject,
                    year=get('year'),
                    number=get('number'),
                    road=get('road'),
                    suburb=get('suburb'),
                    area=get('area'),
                    province=get('province'),
                    olat=floatnone(get('lat')),
                    olong=floatnone(get('lon')),
                )
                addr.save()
                
                if ((naddr+uaddr) % 1000) == 0:
                    transaction.commit()
             
            transaction.commit()
            print '%d New, %d Updated' % (naddr, uaddr)
