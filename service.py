#!/usr/bin/env python3

from datetime import datetime

import logging
log = logging.getLogger()

import geolocator as locator

import persistence

from db import geocoord_format

def search_location(address: str):
    location = persistence.get_location_by_address(address)
    if not location:
        # print('import')
        rloc = locator.geocode(address)
        if not rloc:
            return None
        location = persistence.upsert_location(address, rloc.latitude, rloc.longitude)

    return location

def query_location(address: str = None, latitude: float = None, longitude: float = None):
    if address:
        if latitude and longitude:
            location = persistence.upsert_location(address, latitude, longitude)
        else:
            location = search_location(address)
    else:
        location = persistence.get_all_locations()

    return location
