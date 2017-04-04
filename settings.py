from os import path

#host = '185.80.0.213'
host = 'localhost'
port = 8088
curdir = path.dirname(path.realpath(__file__))
path.curdir = curdir
db_path = 'sqlite:///' + curdir + '/locations.db'

