#!/usr/bin/env python

import os.path

print os.path.realpath(os.path.curdir)
print os.path.realpath(__file__)
print os.path.dirname(os.path.realpath(__file__))
os.path.curdir = os.path.dirname(os.path.realpath(__file__))
print os.path.realpath(os.path.curdir)
