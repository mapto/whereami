from os import path

date_format = "%d/%m/%Y"

#host = '185.80.0.213'
host = 'localhost'
port = 8000

curdir = path.dirname(path.realpath(__file__))
path.curdir = curdir
db_path = 'sqlite:///' + curdir + '/locations.db'
static_path = curdir + '/static'

debug = False
