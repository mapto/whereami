#!/usr/bin/env python3

from datetime import datetime
'''
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime
'''
from settings import debug
from settings import db_path, date_format

from db import Base, engine, Session
from db import Locations

'''
Create all our declared tables
'''
Base.metadata.create_all(engine)

'''
Create session
'''
session = Session()

'''
Create a entries in the Locations table
'''
mecca = Locations(name="Mecca", latitude=21.389082, longitude=39.857912)
new_york = Locations(name="New York", latitude=40.712784, longitude=-74.005941)
berlin = Locations(name="Berlin", latitude=52.520007, longitude=13.404954)
london = Locations(name="London", latitude=51.507351, longitude=-0.127758)
milano = Locations(name="Milano", latitude=45.465422, longitude=9.185924)
sofia = Locations(name="Sofia", latitude=42.697708, longitude=23.321868)
brasilia = Locations(name="Brasilia", latitude=-14.235004, longitude=-51.92528)


session.add_all([mecca, new_york, berlin, london, milano, brasilia])

'''
Commit to the DB
'''
session.commit()
