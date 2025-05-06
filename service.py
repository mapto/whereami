#!/usr/bin/env python3

from datetime import datetime
from urllib.parse import unquote

import geolocator as locator

from settings import debug

from db import Session
from db import Location


def loc2csv(loc):
    return "%.2f,%.2f" % (getattr(loc, "latitude"), getattr(loc, "longitude"))


def to_csv(model):
    """Returns a CSV representation of an SQLAlchemy-backed object."""

    if not model:
        return ""
    if isinstance(model, list):
        return "\n".join([next.name + ", " + loc2csv(next) for next in model if next.latitude and next.longitude])
    else:
        return loc2csv(model)


def query_location(name=None, latitude=None, longitude=None):
    location = None
    session = Session(expire_on_commit=False)
    if name is not None and len(name) > 0:
        name = unquote(name)
        location = session.query(Location).filter(Location.name.like(name)).first()
        if (
            latitude is not None
            and len(latitude) > 0
            and longitude is not None
            and len(longitude) > 0
        ):
            if location is None:
                # print('create')
                location = Location(
                    name=name.upper(), latitude=latitude, longitude=longitude
                )
                session.add(location)
            else:
                # print('update')
                location.latitude = latitude
                location.longitude = longitude
                location.lastseen = datetime.now()
            session.commit()

        else:  # not on our database
            if location is None:
                # print('import')
                rloc = locator.geocode(name)
                location = Location(
                    name=name.upper(), latitude=rloc.latitude, longitude=rloc.longitude
                )
                session.add(location)
                session.commit()
    else:
        location = session.query(Location).order_by(Location.name.asc()).all()

    session.close()
    if not location:
        return None
    print(repr(location))
    return to_csv(location)


if __name__ == "__main__":
    pass
