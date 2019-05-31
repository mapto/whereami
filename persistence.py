import os
from datetime import datetime

import logging
log = logging.getLogger()

from util import normalize, hash

from db import Session, Base, engine
from db import Location, Query

from config import db_path, db_url, dateformat_log


def _set_location(s: Session, address: str, latitude: float, longitude: float, name: str = None) -> Location:
    if not name:
        name = address
    location = Location(name=name, address=address, latitude=latitude, longitude=longitude)
    s.add(location)
    return location

def _get_one_query(s: Session, hashcode: str, provider: str) -> Query:
    return s.query(Query).filter(Query.hashcode == hashcode, Query.provider == provider).first()

def _get_one_location(s: Session, key: str) -> Location:
    return s.query(Location).filter(Location.name.like(key) | Location.address.like(key)).first()

def _get_all_locations(s: Session):
    return s.query(Location).order_by(Location.name.asc()).all()


def cached_query(address: str, provider):
    """Pecondition: provider is one of geopy.geocoders"""
    address = normalize(address)
    provider_name = provider.__class__.__name__
    hashcode = hash(address)

    session = Session(expire_on_commit=False)
    cached = _get_one_query(session, hashcode, provider_name)
    if not cached:
        try:
            log.debug("Querying %s\t%s"%(provider_name, address))
            response = provider.geocode(address)
        except Exception as e:
            print(e)
            response = None
        if response:
            log.debug("Resulted %.2f %.2f"%(response.latitude, response.longitude))
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
    address = normalize(address)
    session = Session(expire_on_commit=False)
    locations = _get_one_location(session, address)
    session.close()

    return locations

def upsert_location(address: str, latitude: float, longitude: float, name: str = None):
    address = normalize(address)
    if not name:
        name = address
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


def reset_db(blank=False, backup=True):
    timestamp = None
    if backup and os.path.exists(db_path):
        timestamp = datetime.now().strftime(dateformat_log)
        backup = "%s.%s.%s" % (db_path[:-3], timestamp, db_path[-2:])
        print("Backup previous database at: %s" % backup)
        os.rename(db_path, backup)

    print("Create new database: %s" % db_url)
    Base.metadata.create_all(engine)

    print("Populate with dummy data: %s" % ('True' if not blank else 'False'))
    if not blank:
        s = Session()
        _set_location(s, "MECCA", latitude=21.389082, longitude=39.857912)
        _set_location(s, "BERLIN", latitude=52.520007, longitude=13.404954)
        _set_location(s, "LONDON", latitude=51.507351, longitude=-0.127758)
        _set_location(s, "MILANO", latitude=45.465422, longitude=9.185924)
        _set_location(s, "SOFIA", latitude=42.697708, longitude=23.321868)
        _set_location(s, "BRASILIA", latitude=-14.235004, longitude=-51.92528)
        s.commit()

    return timestamp

def restore_db(timestamp):
    engine.dispose()

    path = "%s.%s.%s" % (db_path[:-3], timestamp, db_path[-2:]) if timestamp else ""
    if os.path.exists(path):
        timestamp = datetime.now().strftime(dateformat_log)
        os.remove(db_path)
        print("Restoring previous database from: %s" % path)
        os.rename(path, db_path)

if __name__ == '__main__':
    reset_db(blank=True)

