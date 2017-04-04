#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bottle import route, run, template, static_file, get
from bottle import response, request, redirect, error, abort
from urllib import unquote_plus as unquote
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3

from settings import curdir, db_path, host, port
from db import Locations

print ("Working in " + curdir)
engine = create_engine(db_path, echo=False)

Session = sessionmaker(bind=engine)

locator = GoogleV3()

def loc2csv(loc):
    return "%s,%s"%(getattr(loc, "latitude"),getattr(loc, "longitude"))

def to_csv(model):
    """ Returns a CSV representation of an SQLAlchemy-backed object.
    """

    if not model:
        return ""
    if isinstance(model, list):
        return "\n".join([next.name + ", " + loc2csv(next) for next in model])
    else:
        return loc2csv(model)

@error(405)
def mistake405(code):
    return 'The given call is not allowed by the application.'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist.'

@route('/at') # ?name=:name&latitude=:latitude&longitude=:longitude
def query_location_get():
    name = request.query.get("name")
    if name is not None and type(name) is str and len(name) > 0:
        latitude = request.query.get("latitude")
        longitude = request.query.get("longitude")
        if latitude is not None and type(latitude) is str and len(latitude) > 0 and \
           longitude is not None and type(longitude) is str and len(longitude) > 0:
            return query_location(name, latitude, longitude)
        else:
            return query_location(name)
    else:
        return query_location()

@route('/where/:name', method=['GET'])
@route('/where/:name/', method=['GET'])
def get_location(name = None, latitude = None, longitude = None):
    if name is not None and type(name) is str and len(name) > 0:
        return query_location(name)
    else:
        return query_location()

@route('/where', method=['GET'])
@route('/where/', method=['GET'])
@route('/where/:name/:latitude/:longitude', method=['GET', 'POST']) # ?name=:name&latitude=:latitude&longitude=:longitude
def query_location(name = None, latitude = None, longitude = None):
    location = None
    session = Session()
    if name is not None and len(name) > 0:
        name = unquote(name)
        location = session.query(Locations).filter(Locations.name.like(name)).first()
        if latitude is not None and len(latitude) > 0 and longitude is not None and len(longitude) > 0:
            if location is None:
                # print('create')
                location = Locations(name=name, latitude=latitude, longitude=longitude)
                session.add(location)
                session.commit()
            else:
                # print('update')
                location.latitude = latitude
                location.longitude = longitude
                location.lastseen = datetime.now()
                session.commit()
        else: # not on our database
            if location is None:
                # print('import')
                rloc = locator.geocode(name)
                location = Locations(name=name, latitude=rloc.latitude, longitude=rloc.longitude)
                session.add(location)
                session.commit()
    else:
        location = session.query(Locations).all()

    return to_csv(location)
'''
@route('/delete/:name')
def delete_location(name=None):
    session = Session()
    if name is not None and len(name) > 0:
        location = session.query(Locations).filter(Locations.name.like(name)).first()
        if location is not None:
            session.delete(location)
            session.commit()
            return "Successfully deleted: " + name

    return "Nothing to delete"
'''
@route('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')


@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')


@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')


@get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='static/fonts')

@route('/')
def root():
    """ The pages need to be served too, so I added this.
    """
    return static_file('index.html', root=curdir + '/static')

print("Starting in %s"%curdir)
print("With database %s"%db_path)
run(host=host, port=port)