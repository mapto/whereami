#!/usr/bin/env python3

from bottle import Bottle
from bottle import template, static_file
from bottle import response, request, redirect, abort

from settings import debug
from settings import static_path, host, port

import service

app = Bottle(__name__)


@app.error(405)
def mistake405(code):
    return "The given call is not allowed by the application."


@app.error(404)
def mistake404(code):
    return "Sorry, this page does not exist."


@app.get("/at")  # ?name=:name&latitude=:latitude&longitude=:longitude
def query_location_get():
    name = request.query.get("name")
    if name is not None and type(name) is str and len(name) > 0:
        latitude = request.query.get("latitude")
        longitude = request.query.get("longitude")
        if (
            latitude is not None
            and len(latitude) > 0
            and longitude is not None
            and len(longitude) > 0
        ):
            return service.query_location(name, latitude, longitude)
        else:
            return service.query_location(name)
    else:
        return service.query_location()


@app.get("/where")
# @app.get('/where/')
@app.get("/where/:name")
@app.get("/where/:name/")
@app.route(
    "/where/:name/:latitude/:longitude", method=["GET", "POST", "PUT"]
)  # ?name=:name&latitude=:latitude&longitude=:longitude
def query_location(name=None, latitude=None, longitude=None):
    if name is not None and type(name) is str and len(name) > 0:
        if (
            latitude is not None
            and len(latitude) > 0
            and longitude is not None
            and len(longitude) > 0
        ):
            return service.query_location(name, latitude, longitude)
        else:
            return service.query_location(name)
    else:
        return service.query_location()


"""
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
"""


@app.get("/<filename:re:.*\.js>")
def javascripts(filename):
    return static_file(filename, root=static_path + "/js")


@app.get("/<filename:re:.*\.css>")
def stylesheets(filename):
    return static_file(filename, root=static_path + "/css")


@app.get("/<filename:re:.*\.(jpg|png|gif|ico)>")
def images(filename):
    return static_file(filename, root=static_path + "/img")


@app.get("/<filename:re:.*\.(eot|ttf|woff|svg)>")
def fonts(filename):
    return static_file(filename, root=static_path + "/fonts")


@app.get("/")
def root():
    return static_file("index.html", root=static_path)


def start_server():
    import os

    from settings import curdir, db_url

    from db import reset_db

    print("Starting in %s" % curdir)
    if os.path.exists(db_url):
        print("With database %s" % db_url)
    else:
        reset_db(blank=True)
    app.run(host=host, port=port, debug=debug, reload=True)


if __name__ == "__main__":
    start_server()
