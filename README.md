# whereami - A web service for GAZE BEYOND

In memory of Liana Lessa (1987-2017).

On 21 January 2019 I have decided that the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) license better serves the memory of Liana. It would still allow people to reuse this code, but would also make sure that they mention this site as a source and thus would keep her memory alive. For obvious legal reasons, the code up to the [tag:gaze_beyond](https://github.com/mapto/whereami/releases/tag/gaze_beyond) is also available under the [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html) as previously.

This is a test service for her prototype for http://cargocollective.com/lialessa/GAZE-BEYOND, probably the best use of geolocation I've encountered in my life. Please do check out the idea and - if inspired - do try to take it forward, with or without me.

## Requirements
- Python3 (https://www.python.org)
- bottle (http://bottlepy.org)
- SQLAlchemy (http://www.sqlalchemy.org) using SQLite (https://sqlite.org)
- GeoPy (https://github.com/geopy) using ArcGIS (https://www.arcgis.com)
- NumPy (https://numpy.org/)
- jQuery (https://jquery.com/)
- Bootstrap (https://getbootstrap.com/)
- Leaflet (https://leafletjs.com/)

## Executables
- To test web services, run "python test.py".
- To create a blank database run "python db.py".
- To start the API locally, run "python main.py" and open http://localhost:8000 from your browser. All major browsers are supported.
- Use 'pyinstaller main.spec' to build a standalone executable (requries [pyinstaller](https://www.pyinstaller.org/)). This [requires](https://github.com/mapto/whereami/blob/master/main.spec) a database file.
- Use 'docker compose up' to deploy a docker container (requries [docker compose](https://docs.docker.com/compose/)).

## API GET endpoints
* **/at** - get all locations<br/>
* **/at?name=sofia** - get locations like name<br/>
* **/at?name=sofia&latitude=42.7&longitude=23** - set location of name to the given coordinates<br/>
* **/where** - same as **/at**<br/>
* **/where/sofia** - same as **/at?name=sofia**<br/>
* **/where/sofia/42.7/23** - same as **/at?name=sofia&latitude=42.7&longitude=23**<br/>

The service has a web interface, but was intended to be accessed from Arduino. Thus, it serves GET endpoints also for PUT operations. For the same reason it also delivers CSV, and not JSON.

To see the web interface, visit http://whereami.unriddle.it.
