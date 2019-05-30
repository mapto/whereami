from os import path

date_format = "%d/%m/%Y"
dateformat_log = "%Y%m%d%H%M%S"

coord_format = "{:.2f}"
geocoord_format = "{},{}".format(coord_format, coord_format)

#host = '185.80.0.213'
host = 'localhost'
port = 8000

curdir = path.dirname(path.realpath(__file__)) # no trailing slash
path.curdir = curdir
db_path = curdir + '/data/locations.db'
db_url = 'sqlite:///' + db_path + '?check_same_thread=False'

static_path = curdir + '/static'

import logging
log = logging.getLogger()
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)
