#!/usr/bin/env python3

from datetime import datetime

from typing import List
from db import Location

import logging
log = logging.getLogger()

import geolocator as locator

import persistence

from db import geocoord_format

def search_location(address: str) -> Location:
    location = persistence.get_location_by_address(address)
    if not location:
        # print('import')
        rloc = locator.geocode(address)
        if not rloc:
            return None
        location = persistence.upsert_location(address, rloc.latitude, rloc.longitude)

    return location

def query_location(address: str = None, latitude: float = None, longitude: float = None) -> List[Location]:
    if address:
        if latitude and longitude:
            locations = [persistence.upsert_location(address, latitude, longitude)]
        else:
            locations = [search_location(address)]
    else:
        locations = persistence.get_all_locations()

    return locations
