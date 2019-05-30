#!/usr/bin/env python3
"""Run standalone to reset DB for test purposes. Timestamped backup of previous version will be created if it exists"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, func

import logging
log = logging.getLogger()

from config import db_url, coord_format, geocoord_format


Base = declarative_base()

engine = create_engine(db_url, echo=(log.getEffectiveLevel() <= logging.DEBUG))


class Query(Base):
    """Queries are agnostic to names"""
    __tablename__ = 'query'

    id = Column(Integer, primary_key=True)
    hashcode = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    provider = Column(String, default=None)
    date = Column(DateTime, default=func.current_timestamp(), nullable=False)


class Location(Base):
    """When a name is missig, it should be made equal to the address"""
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    address = Column(String, default=None, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    lastseen = Column(DateTime, default=func.current_timestamp(), nullable=False)

    def json(self):
        return {"name": self.name, "address": self.address, "latitude": coord_format.format(self.latitude), "longitude": coord_format.format(self.longitude)}

    def __repr__(self):
        return "{:json}".format(self)

    def __format__(self, format):
        if format == 'coord':
            return geocoord_format.format(self.latitude, self.longitude)
        if format == 'csv':
            return '{} ({:coord}): "{}"'.format(self.name, self, self.address)
        if format == 'json':
            return str(self.__dict__)


Session = sessionmaker(bind=engine)

# session = Session()

