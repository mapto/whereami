import hashlib
import re

import numpy as np

# The geolocators in geopy that do not expect api_key
from geopy.geocoders import GeocodeFarm, Yandex, ArcGIS

from db import Session
from db import Query

locators = [GeocodeFarm(), Yandex(), ArcGIS()]

def _query(session, hashcode, provider):
    return session.query(Query).filter(Query.hashcode == hashcode, Query.provider == provider).first()

def cached_query(address, provider):
    address = re.sub(r'\s+', ' ', address.upper())
    session = Session(expire_on_commit=False)
    provider_name = provider.__class__.__name__
    hashcode = hashlib.md5(bytes(address, encoding="utf-8")).hexdigest()
    cached = _query(session, hashcode, provider_name)
    if not cached:
        try:
            response = provider.geocode(address)
        except Exception as e:
            print(e)
            response = None
        if response:
            cached = Query(hashcode=hashcode, address=address,\
                latitude=response.latitude, longitude=response.longitude,\
                provider=provider_name)
            session.add(cached)
            session.commit()

    #session.expunge(cached)
    #session.expunge_all()
    session.close()
    return cached

class Coordinates:
    def __init__(self, latitude, longitude):
        self.latitude=latitude
        self.longitude=longitude

    def __repr__(self):
        return "%s, %s" %(self.latitude, self.longitude)

def reject_outliers(data, alpha = 90):
    mask = (data.lat < np.percentile(data.lat, alpha)) & (data.long < np.percentile(data.long, alpha))
    return data[mask]

def geocode(address):
    #candidates = np.array([], dtype=[('long',float),('lat', float)])
    candidates = []
    for locator in locators:
        rloc = cached_query(address, locator)
        if rloc:
            #print(rloc.raw)
            candidates.append((rloc.latitude, rloc.longitude))
            #coords = np.core.records.fromrecords([x.values() for x in candidates], names=candidates[0].keys())
            #candidates.append(rloc)
            #a = np.array([(1, 2.0), (1, 2.0)], dtype=[('x', int), ('y', float)])
    if not candidates:
        return None
    
    coords = np.core.records.fromrecords(candidates, names='lat,long')
    if len(coords) > 2:
        coords = reject_outliers(coords)
    #return {"latitude": np.average(coords.lat), "longitude": np.average(coords.long)}
    return Coordinates(np.average(coords.lat), np.average(coords.long))

if __name__ == '__main__':
    result = geocode("VIA DELLA CASETTA MATTEI 205")
    print(result)
