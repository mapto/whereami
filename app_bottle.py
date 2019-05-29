#!/usr/bin/env python3

from bottle import Bottle
from bottle import static_file, request, abort

from config import debug
from config import static_path, host, port

import service

app = Bottle()

@app.get('/at') # ?name=:name&latitude=:latitude&longitude=:longitude
def query_location_get():
    name = request.query.get("name")
    if name is not None and type(name) is str and len(name) > 0:
        latitude = request.query.get("latitude")
        longitude = request.query.get("longitude")
        if latitude is not None and len(latitude) > 0 and \
           longitude is not None and len(longitude) > 0:
            result = service.query_location(name, latitude, longitude)
        else:
            result = service.query_location(name)
    else:
        result = service.query_location()
    if not result:
        abort(404)
    return result


@app.get('/where')
@app.get('/where/')
@app.get('/where/:name')
@app.get('/where/:name/')
@app.get('/where/:name/:latitude/:longitude') # ?name=:name&latitude=:latitude&longitude=:longitude
@app.post('/where/:name/:latitude/:longitude') # ?name=:name&latitude=:latitude&longitude=:longitude
@app.put('/where/:name/:latitude/:longitude') # ?name=:name&latitude=:latitude&longitude=:longitude
def query_location(name: str = None, latitude: float = None, longitude: float = None):
    if name is not None and type(name) is str and len(name) > 0:
        if latitude is not None and len(latitude) > 0 and \
           longitude is not None and len(longitude) > 0:
            result = service.query_location(name, latitude, longitude)
        else:
            result = service.query_location(name)
    else:
        result = service.query_location()
    if not result:
        abort(404)
    return result

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
@app.get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root=static_path + '/js')


@app.get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root=static_path + '/css')


@app.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root=static_path + '/img')


@app.get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root=static_path + '/fonts')

@app.get('/')
def root():
    return static_file('index.html', root=static_path)

def start_server():
    import os

    from config import curdir, db_url, db_path
    
    print("Starting in %s"%curdir)
    if os.path.exists(db_path):
        print("With database %s"%db_url)
    else:
        from db import reset_db
        reset_db(blank=True)
    app.run(host=host, port=port, debug=debug, reload=True)

if __name__ == '__main__':
    start_server()
      