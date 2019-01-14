#!/usr/bin/env python3

from bottle import route, run, template, static_file, get
from bottle import response, request, redirect, error, abort

from settings import debug
from settings import static_path, host, port

import service

@error(405)
def mistake405(code):
    return 'The given call is not allowed by the application.'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist.'

@route('/at', method=['GET']) # ?name=:name&latitude=:latitude&longitude=:longitude
def query_location_get():
    name = request.query.get("name")
    if name is not None and type(name) is str and len(name) > 0:
        latitude = request.query.get("latitude")
        longitude = request.query.get("longitude")
        if latitude is not None and len(latitude) > 0 and \
           longitude is not None and len(longitude) > 0:
            return service.query_location(name, latitude, longitude)
        else:
            return service.query_location(name)
    else:
        return service.query_location()

@route('/where', method=['GET'])
@route('/where/', method=['GET'])
@route('/where/:name', method=['GET'])
@route('/where/:name/', method=['GET'])
@route('/where/:name/:latitude/:longitude', method=['GET', 'POST', 'PUT']) # ?name=:name&latitude=:latitude&longitude=:longitude
def query_location(name = None, latitude = None, longitude = None):
    if name is not None and type(name) is str and len(name) > 0:
        if latitude is not None and len(latitude) > 0 and \
           longitude is not None and len(longitude) > 0:
            return service.query_location(name, latitude, longitude)
        else:
            return service.query_location(name)
    else:
        return service.query_location()

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
    return static_file(filename, root=static_path + '/js')


@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root=static_path + '/css')


@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root=static_path + '/img')


@get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root=static_path + '/fonts')

@route('/')
def root():
    return static_file('index.html', root=static_path)

def start_server():
    import os

    from settings import curdir, db_url
    
    from db import reset_db

    print("Starting in %s"%curdir)
    if os.path.exists(db_url):
        print("With database %s"%db_url)
    else:
        reset_db(blank=True)
    run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    start_server()
    