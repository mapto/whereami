# whereami - A web service for GAZE BEYOND

In memory of Liana Lessa (1987-2017).

This is a test service for her prototype for http://cargocollective.com/lialessa/GAZE-BEYOND

Requirements:
- Python 3 (https://www.python.org)
- bottle (http://bottlepy.org)
- SQLAlchemy (http://www.sqlalchemy.org) using SQLite (https://sqlite.org)
- GeoPy (https://github.com/geopy) using GeocodeFarm (https://geocode.farm)

To fill the database with dummy data run "python setup_db.py". Then to start the API locally, run "python main.py" and open http://localhost:8000 from your browser. All major browsers are supported.

The API will give you access to the following GET endpoints:<br/>
/at<br/>
/at?name=sofia<br/>
/at?name=sofia&latitude=42.7&longitude=23<br/>
/where<br/>
/where/sofia<br/>
/where/sofia/42.7/23<br/>

The service has a web interface, but was intended to be accessed from Arduino. Thus, for convenience some services deliver CSV, and not JSON. To see the web interface, visit http://whereami.unriddle.it.
