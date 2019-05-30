# whereami - A web service for GAZE BEYOND

In memory of Liana Lessa (1987-2017).

On 21 January 2019 I have decided that the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) license better serves the memory of Liana. It would still allow people to reuse this code, but would also make sure that they mention this site as a source and thus would keep her memory alive. For obvious legal reasons, the code up to the [tag:gaze_beyond](https://github.com/mapto/whereami/releases/tag/gaze_beyond) is also available under the [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html) as previously.

This is a test service for her prototype for http://cargocollective.com/lialessa/GAZE-BEYOND

## Requirements
- Python3 (https://www.python.org)
- bottle (http://bottlepy.org)
- SQLAlchemy (http://www.sqlalchemy.org) using SQLite (https://sqlite.org)
- GeoPy (https://github.com/geopy) using GeocodeFarm (https://geocode.farm), ArcGIS (https://www.arcgis.com) and Yandex (https://yandex.com/maps/)

## Executables
- To test web services, run "python test.py".
- To create a blank database run "python db.py".
- To start the API locally, run "python app_bottle.py" and open http://localhost:8000 from your browser. All major browsers are supported.
- Use 'pyinstaller bottle.spec' to build a standalone executable (requries [pyinstaller](https://www.pyinstaller.org/)). This [requires](https://github.com/mapto/whereami/blob/master/bottle.spec) a database file.

## API GET endpoints
* **/at** - get all locations<br/>
* **/at?name=sofia** - get locations like name<br/>
* **/at?name=sofia&latitude=42.7&longitude=23** - set location of name to the given coordinates<br/>
* **/where** - same as **/at**<br/>
* **/where/sofia** - same as **/at?name=sofia**<br/>
* **/where/sofia/42.7/23** - same as **/at?name=sofia&latitude=42.7&longitude=23**<br/>

The service has a web interface, but was intended to be accessed from Arduino. Thus, it serves GET endpoints also for PUT operations.

To see the web interface, visit http://whereami.unriddle.it.
