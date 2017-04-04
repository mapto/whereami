# whereami - A web service for GAZE BEYOND

In memory of Liana Lessa (1987-2017).

This is a test service for her prototype for http://lialessa.com/GAZE-BEYOND

Requirements:
- SQLite (https://sqlite.org/)
- Python 2.7 (https://www.python.org/)
- bottle (http://bottlepy.org/)
- SQLAlchemy (http://www.sqlalchemy.org/)
- python-ujson (https://pypi.python.org/pypi/ujson)

To fill the database with dummy data run "python setup_db.py". Then to start the API locally, run "python main.py" and open http://localhost:8088 from your browser. All major browsers should be supported.

The API will give you access to the following GET endpoints:
/at
/at?name=sofia
/at?name=sofia&latitude=42.7&longitude=23
/where
/where/sofia
/where/sofia/42.7/23

The service has a web interface, but was intended to be accessed from Arduino. Thus, for convenience some services deliver CSV, and not JSON. To see the web interface, visit http://whereami.unriddle.it.
