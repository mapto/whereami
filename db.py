from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, func

from settings import db_path
from settings import debug

'''
Declare Tables
'''
Base = declarative_base()

engine = create_engine(db_path, echo=False)


class Locations(Base):
    __tablename__ = 'Locations'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    address = Column(String, default=None)
    latitude = Column(Float)
    longitude = Column(Float)
    lastseen = Column(DateTime, default=func.current_timestamp())

Session = sessionmaker(bind=engine)
