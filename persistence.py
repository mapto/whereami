from urllib.parse import unquote
import hashlib
import re

from db import Session
from db import Location, Query

def _set_location(s: Session, address: str, latitude: float, longitude: float, name: str = None) -> Location:
    if not name:
        name = address
    location = Location(name=name, address=address, latitude=latitude, longitude=longitude)
    s.add(location)
    return location

def _get_one_query(s: Session, hashcode: str, provider: str) -> Query:
    return s.query(Query).filter(Query.hashcode == hashcode, Query.provider == provider).first()

def _get_one_location(s: Session, name: str) -> Location:
    return s.query(Location).filter(Location.name.like(name)).first()

def _get_all_locations(s: Session) -> Location:
    return s.query(Location).order_by(Location.name.asc()).all()

def cached_query(address: str, provider: str = None):
    address = re.sub(r'\s+', ' ', address.upper())  # normalise address
    session = Session(expire_on_commit=False)
    provider_name = provider.__class__.__name__
    hashcode = hashlib.md5(bytes(address, encoding="utf-8")).hexdigest()
    cached = _get_one_query(session, hashcode, provider_name)
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

def get_all_locations():
    session = Session(expire_on_commit=False)
    locations = _get_all_locations(session)
    session.close()

    return locations

def get_location_by_address(address: str):
    address = re.sub(r'\s+', ' ', address.upper())  # normalise address
    session = Session(expire_on_commit=False)
    locations = _get_one_location(session, address)
    session.close()

    return locations

def upsert_location(address: str, latitude: float, longitude: float, name: str = None):
    if not name:
        name = address
    name = unquote(name).upper()  # normalise name
    session = Session(expire_on_commit=False)
    location = _get_one_location(session, name)
    if location:
        # print('update')
        location.latitude = latitude
        location.longitude = longitude
        location.lastseen = datetime.now()
    else:
        # print('create')
        location = _set_location(session, address=address, name=name, latitude=latitude, longitude=longitude)
        session.add(location)
    session.commit()
    session.close()

    return location

