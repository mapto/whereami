import numpy as np

from persistence import cached_query

from db import geocoord_format

from secret import selected_locators

import logging
log = logging.getLogger()

class Coordinates:
    def __init__(self, latitude, longitude):
        self.latitude=latitude
        self.longitude=longitude
    """
    def __repr__(self):
        return "%s, %s" %(self.latitude, self.longitude)
    """
    def __format__(self, format):
        if format == 'csv':
            return geocoord_format.format(self.latitude, self.longitude)
        if format == 'json':
            return json.dumps(self)

def reject_outliers(data, alpha = 90):
    mask = (data.lat < np.percentile(data.lat, alpha)) & (data.long < np.percentile(data.long, alpha))
    return data[mask]

def geocode(address, name=None, locators=None):
    if not name:
        name = address
    if not locators:
        locators = selected_locators.values()    
    #candidates = np.array([], dtype=[('long',float),('lat', float)])
    candidates = []
    for locator in locators:
        log.debug(locator.__class__.__name__)
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
    # result = geocode(u"VIA DELLA CASETTA MATTEI 205", locators=allGeocoders())
    # addr = "VIA DELLA CASETTA MATTEI 205"
    addr = u"I-ва МБАЛ бул. П. Евтимий №37, СРЕДЕЦ, СОФИЯ"
    result = geocode(addr)
    log.info(geocoord_format.format(result.latitude, result.longitude))
