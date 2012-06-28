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
        if a in ['road','suburb','area','province']:
            if v == '98' or v == '99':
                return 0
        if a in ['postcode']:
            try:
                v = int(v)
            except:
                try:
                    v = int(v[1:])
                except:
                    print v
                    v = None
        
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
    
    return str(datarow[index])

def province(s):
    p = var(s)
    if p is None:
        return None
    if p.lower() == 'gp':
        p = 'Gauteng'
    return p

def migrate(s):
    if str(s) == '1':
        return True
    if str(s) == '0':
        return False
    return None

datafolder = '%s/data/' % (settings.PROJECT_ROOT)

dataorder = [
    # Addresses
    'yr14 bt20 addresses and migration codes 24 march 2009.csv',
    'yr18 migration updated feb 09 2012.csv',
    
    # GPS Data
    #'Year 13 Mobile Adol Section 1 GPS Coordinates.csv',
    #'Yr15 GPS Dates updated (5th Jun 09)1 Active.csv',
    #'Yr 16 GPS Updated Dates (active) 9 Jun 091.csv',
    
    # Validated Data
    '3273 homes of non-movers Nov 4 2011.csv',
]

datamap = {
    'yr18 migration updated feb 09 2012.csv': [
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2004),
            'number': (var, 'Y14 House Number'),
            'road': (var, 'Y14 Street Name'),
            'suburb': (var, 'Y14 Suburb'),
            'area': (var, 'Y14 Area/Zone'),
            'province': (province, 'Y14 Province'),
            'postcode': None,
            'migrated': None,
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2004),
            'number': (var, 'Yr18_2004Add1_HouseNumber'),
            'road': (var, 'Yr18_2004Add1_StreetName'),
            'suburb': (var, 'Yr18_2004Add1_Suburb'),
            'area': (var, 'Yr18_2004Add1_Area/Zone'),
            'province': (province, 'Yr18_2004Add1_Province'),
            'postcode': None,
            'migrated': None,
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2005),
            'number': (var, 'Y15_House .'),
            'road': (var, 'Y15_ Street Name'),
            'suburb': (var, 'Y15_Suburb'),
            'area': (var, 'Y15_Town/Post_Office'),
            'province': None,
            'postcode': (var, 'Y15_Code'),
            'migrated': None,
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2005),
            'number': (var, 'Yr18_2005Add2_HouseNumber'),
            'road': (var, 'Yr18_2005Add2_StreetName'),
            'suburb': (var, 'Yr18_2005Add2_Suburb'),
            'area': (var, 'Yr18_2005Add2_Area/Zone'),
            'province': (province, 'Yr18_2005Add2_Province'),
            'postcode': None,
            'migrated': (var, 'Yr18_2005Add2_Move'),
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2006),
            'number': (var, 'Y16_House .'),
            'road': (var, 'Y16_Street Name'),
            'suburb': (var, 'Y16_Suburb'),
            'area': (var, 'Y16_ Town/Post_Office'),
            'province': None,
            'postcode': (var, 'Y16_Code'),
            'migrated': None,
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2006),
            'number': (var, 'Yr18_2006Add3_HouseNumber'),
            'road': (var, 'Yr18_2006Add3_StreetName'),
            'suburb': (var, 'Yr18_2006Add3_Suburb'),
            'area': (var, 'Yr18_2006Add3_Area/Zone'),
            'province': (province, 'Yr18_2006Add3_Province'),
            'postcode': None,
            'migrated': (var, 'Yr18_2006Add3_Move'),
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2007),
            'number': (var, 'Y17_House .'),
            'road': (var, 'Y17_Street Name'),
            'suburb': (var, 'Y17_Suburb'),
            'area': (var, 'Y17_ Town/Post_Office'),
            'province': None,
            'postcode': (var, 'Y17_ Code'),
            'migrated': None,
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2007),
            'number': (var, 'Yr18_2007Add4_HouseNumber'),
            'road': (var, 'Yr18_2007Add4_StreetName'),
            'suburb': (var, 'Yr18_2007Add4_Suburb'),
            'area': (var, 'Yr18_2007Add4_Area/Zone'),
            'province': (province, 'Yr18_2007Add4_Province'),
            'postcode': None,
            'migrated': (var, 'Yr18_2007Add4_Move'),
            'lat': None,
            'lon': None,
        },
    ],
    'yr14 bt20 addresses and migration codes 24 march 2009.csv': [
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 1990),
            'number': (var, 'ANTENATA'),
            'road': (var, 'V5_A'),
            'suburb': (var, 'V6_A'),
            'area': (var, 'V7_A'),
            'province': (province, 'V8_A'),
            'postcode': None,
            'migrated': None,
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 1991),
            'number': (var, 'Y1HOUSEN'),
            'road': (var, 'Y1STREET'),
            'suburb': (var, 'Y1SUBURB'),
            'area': (var, 'Y1AREAZO'),
            'province': (province, 'Y1PROVIN'),
            'postcode': None,
            'migrated': (migrate, 'Y1MIGRAT'),
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 1992),
            'number': (var, 'Y2HOUSEN'),
            'road': (var, 'Y2STREET'),
            'suburb': (var, 'Y2SUBURB'),
            'area': (var, 'Y2AREAZO'),
            'province': (province, 'Y2PROVIN'),
            'postcode': None,
            'migrated': (migrate, 'Y2MIGRAT'),
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 1993),
            'number': (var, 'Y34HOUSE'),
            'road': (var, 'Y34STREE'),
            'suburb': (var, 'Y34SUBUR'),
            'area': (var, 'Y34AREAZ'),
            'province': (province, 'Y34PROVI'),
            'postcode': None,
            'migrated': (migrate, 'Y34MIGRA'),
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 1995),
            'number': (var, 'Y56HOUSE'),
            'road': (var, 'Y56STREE'),
            'suburb': (var, 'Y56SUBUR'),
            'area': (var, 'Y56AREAZ'),
            'province': (province, 'Y56PROVI'),
            'postcode': None,
            'migrated': (migrate, 'Y56MIGRA'),
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 1997),
            'number': (var, 'Y78HOUSE'),
            'road': (var, 'Y78STREE'),
            'suburb': (var, 'Y78SUBUR'),
            'area': (var, 'Y78AREAZ'),
            'province': (province, 'Y78PROVI'),
            'postcode': None,
            'migrated': (migrate, 'Y78MIGRA'),
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 1999),
            'number': (var, 'Y910HOUS'),
            'road': (var, 'Y910STRE'),
            'suburb': (var, 'Y910SUBU'),
            'area': (var, 'Y910AREA'),
            'province': (province, 'Y910PROV'),
            'postcode': None,
            'migrated': (migrate, 'Y910MIGR'),
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2001),
            'number': (var, 'Y1112HOU'),
            'road': (var, 'Y1112STR'),
            'suburb': (var, 'Y1112SUB'),
            'area': (var, 'Y1112ARE'),
            'province': (province, 'Y1112PRO'),
            'postcode': None,
            'migrated': (migrate, 'Y1112MIG'),
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2003),
            'number': (var, 'Y13HOUSE'),
            'road': (var, 'Y13STREE'),
            'suburb': (var, 'Y13SUBUR'),
            'area': (var, 'Y13AREAZ'),
            'province': (province, 'Y13PROVI'),
            'postcode': None,
            'migrated': (migrate, 'Y13MIGRA'),
            'lat': None,
            'lon': None,
        },
        {
            'bttid': (var, 'BT20ID'),
            'year': (None, 2004),
            'number': (var, 'Y14HOUSE'),
            'road': (var, 'Y14STREE'),
            'suburb': (var, 'Y14SUBUR'),
            'area': (var, 'Y14AREAZ'),
            'province': (province, 'Y14PROVI'),
            'postcode': None,
            'migrated': (migrate, 'Y14MIGRA'),
            'lat': None,
            'lon': None,
        },
    ],
    '3273 homes of non-movers Nov 4 2011.csv': [
        {
            'bttid': (var, 'bttid'),
            'year': (None, 1997),
            'number': (var, 'homenumber'),
            'road': (var, 'homeroad'),
            'suburb': (var, 'homesuburb'),
            'area': (var, 'homearea'),
            'province': (province, 'homeprov'),
            'postcode': None,
            'migrated': None,
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
            'postcode': None,
            'migrated': None,
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
            'postcode': None,
            'migrated': None,
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
            'postcode': None,
            'migrated': None,
            'lat': (var, 'home_lat'),
            'lon': (var, 'home_long'),
        },
    ]
}

def get(attr):
    ret = map[attr]
    if ret is not None:
        (fun, val) = ret
        if fun is None:
            return val
        else:
            return fun(val)
    return None

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
                        subject = Subject.objects.get(bttid=intnone(get('bttid')))
                    except:
                        subject = Subject(bttid=intnone(get('bttid')))
                        subject.save()
    
                    try:
                        addr = Address.objects.get(subject=subject, year=intnone(get('year')))
                        uaddr += 1
                        nutype = 0
                    except:
                        addr = Address(
                            subject=subject,
                            year=intnone(get('year')),
                        )
                        naddr += 1
                        nutype = 1
                    
                    cnt = 0            
                    cnt += setnotnone(addr,'road',get('road'))
                    cnt += setnotnone(addr,'suburb',get('suburb'))
                    cnt += setnotnone(addr,'area',get('area'))
                    
                    num = get('number')
                    if cnt == 0:
                        if num == '98' or num == '99':
                            num = None
                        if str(num).lower().find('missing') != -1:
                            num = None 
                    cnt += setnotnone(addr,'number',num)

                    cnt += setnotnone(addr,'province',get('province'))
                    cnt += setnotnone(addr,'postcode',get('postcode'))
                    cnt += setnotnone(addr,'migrated',get('migrated'))
                    cnt += setnotnone(addr,'lat',floatnone(get('lat')))
                    cnt += setnotnone(addr,'lon',floatnone(get('lon')))
                    
                    if cnt == 0:
                        saddr += 1
                        if nutype == 0:
                            uaddr -= 1
                        else:
                            naddr -= 1
                    else:
                        # Let address get re-generated
                        addr.address = None
                        addr.save()
                    
                    if ((naddr+uaddr) % 1000) == 0:
                        transaction.commit()
                 
                transaction.commit()
                print '%d New, %d Updated, %d Empty' % (naddr, uaddr, saddr)
            
