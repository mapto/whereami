#!/usr/bin/env python3
"""
https://www.cik.bg/upload/83178/Sekcii-IS-05.04.2019-Ep0-BezDop-01.xlsx

0. Област код
1. Област текст
2. Община код
3. Община
4. Район код
5. Район
6. Секция
7. Населено място код
8. Населено място
9. Адрес

"""

import csv
import time

import service, geolocator
import util

import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

srcfile = 'data/sections-sofia.csv'

timeout = 2

def load_data():
    addresses = set()
    sections = {}
    sections2 = {}

    with open(srcfile, 'r', encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar="'")
        for i, row in enumerate(csvreader):
            if i == 0:
                continue;
            if i == 50:
                break;
            section_id = row[6]
            addr_long = "%s, %s, %s"%(row[9],row[5],row[8][3:])
            addr_short = "%s, %s"%(row[9],row[8][3:])
            addresses.add(addr_long)
            addresses.add(addr_short)
            sections[section_id] = addr_long
            sections[section_id] = addr_short
    return addresses

def import_queries(addresses):
    for addr in addresses:
        print(addr)
        geolocator.geocode(addr)
        time.sleep(timeout)

def import_locations(addresses):
    for addr in addresses:
        print(addr)
        service.search_location(addr)
        time.sleep(timeout)

if __name__ == '__main__':
    # import_queries(load_data())
    import_locations(load_data())
