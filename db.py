#!/usr/bin/env python3
"""Run standalone to reset DB for test purposes. Timestamped backup of previous version will be created if it exists"""

import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, func

from settings import db_path, db_url, dateformat_log
from settings import debug

'''
Declare Tables
'''
Base = declarative_base()

engine = create_engine(db_url, echo=False)


class Locations(Base):
    __tablename__ = 'Locations'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    address = Column(String, default=None)
    latitude = Column(Float)
    longitude = Column(Float)
    lastseen = Column(DateTime, default=func.current_timestamp())

Session = sessionmaker(bind=engine)

session = Session()

def reset_db(backup=True):
	timestamp = None
	if backup and os.path.exists(db_path):
		timestamp = datetime.now().strftime(dateformat_log)
		backup = "%s.%s.%s" % (db_path[:-3], timestamp, db_path[-2:])
		print("Backup previous database at: %s" % backup)
		os.rename(db_path, backup)

	print("Create new database: %s" % db_url)
	Base.metadata.create_all(engine)

	mecca = Locations(name="Mecca", latitude=21.389082, longitude=39.857912)
	new_york = Locations(name="New York", latitude=40.712784, longitude=-74.005941)
	berlin = Locations(name="Berlin", latitude=52.520007, longitude=13.404954)
	london = Locations(name="London", latitude=51.507351, longitude=-0.127758)
	milano = Locations(name="Milano", latitude=45.465422, longitude=9.185924)
	sofia = Locations(name="Sofia", latitude=42.697708, longitude=23.321868)
	brasilia = Locations(name="Brasilia", latitude=-14.235004, longitude=-51.92528)

	session.add_all([mecca, new_york, berlin, london, milano, sofia, brasilia])
	session.commit()

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
	reset_db()
