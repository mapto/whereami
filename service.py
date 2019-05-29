#!/usr/bin/env python3

from datetime import datetime

import geolocator as locator

import persistence

def loc2csv(loc):
    return "%.2f,%.2f"%(getattr(loc, "latitude"),getattr(loc, "longitude"))

def to_csv(model):
    """ Returns a CSV representation of an SQLAlchemy-backed object.
    """

    if not model:
        return ""
    if isinstance(model, list):
        return "\n".join([next.name + ", " + loc2csv(next) for next in model])
    else:
        return loc2csv(model)

def search_location(address: str):
    location = persistence.get_location_by_address(address)
    if not location:
        # print('import')
        rloc = locator.geocode(address)
        if not rloc:
            return None
        location = persistence.upsert_location(address, rloc.latitude, rloc.longitude)

    return location

def query_location(name: str = None, latitude: float = None, longitude: float = None):
    if name:
        if latitude and longitude:
            location = persistence.upsert_location(name, latitude, longitude)
        else:
            location = search_location(name)
    else:
        location = persistence.get_all_locations()
    return to_csv(location)
