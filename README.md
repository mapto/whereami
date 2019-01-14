# whereami - A web service for GAZE BEYOND

In memory of Liana Lessa (1987-2017).

This is a test service for her prototype for http://cargocollective.com/lialessa/GAZE-BEYOND

## Requirements
- Python3 (https://www.python.org)
- bottle (http://bottlepy.org)
- SQLAlchemy (http://www.sqlalchemy.org) using SQLite (https://sqlite.org)
- GeoPy (https://github.com/geopy) using GeocodeFarm (https://geocode.farm), ArcGIS (https://www.arcgis.com) and Yandex (https://yandex.com/maps/)

## Executables
- To test web services, run "python test.py".
- To create a blank database run "python db.py".
- To start the API locally, run "python main.py" and open http://localhost:8000 from your browser. All major browsers are supported.
- Use 'pyinstaller main.spec' to build a standalone executable (requries [pyinstaller](https://www.pyinstaller.org/)). This [requires](https://github.com/mapto/whereami/blob/master/main.spec) a database file.

## API GET endpoints
* **/at** - get all locations<br/>
* **/at?name=sofia** - get locations like name<br/>
* **/at?name=sofia&latitude=42.7&longitude=23** - set location of name to the given coordinates<br/>
* **/where** - same as **/at**<br/>
* **/where/sofia** - same as **/at?name=sofia**<br/>
* **/where/sofia/42.7/23** - same as **/at?name=sofia&latitude=42.7&longitude=23**<br/>

The service has a web interface, but was intended to be accessed from Arduino. Thus, it serves GET endpoints also for PUT operations. For the same reason it also delivers CSV, and not JSON.

To see the web interface, visit http://whereami.unriddle.it.
