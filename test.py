#!/usr/bin/env python

"""This is very quick and dirty service testing.
It makes a copy of the database and wipes it.
Also, server remains running at the end and user has to stop it."""

import os
import requests
from threading import Thread
from time import sleep

from bottle import WSGIRefServer, run

from settings import host, port

from db import reset_db, restore_db
from main import start_server

timeout = 3

root_url = "http://%s:%d" % (host, port)

def test_service(url, expected=None):
	response = requests.get(url)
	assert(response.status_code == 200)
	if not expected:
		if response.text:
			print(response.text)
	else:
		assert(response.text == expected)
	return response.text

from threading import Thread
import time

class TestWSGIServer(WSGIRefServer):
	"""A mimic of WSGIRefServer with changes allowing the server to be shutdown wih a dedicated call.
	Taken from https://stackoverflow.com/a/19749945/1827854"""
	def run(self, app): # pragma: no cover
		from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
		from wsgiref.simple_server import make_server
		import socket

		class FixedHandler(WSGIRequestHandler):
			def address_string(self): # Prevent reverse DNS lookups please.
				return self.client_address[0]
			def log_request(*args, **kw):
				if not self.quiet:
					return WSGIRequestHandler.log_request(*args, **kw)

		handler_cls = self.options.get('handler_class', FixedHandler)
		server_cls  = self.options.get('server_class', WSGIServer)

		if ':' in self.host: # Fix wsgiref for IPv6 addresses.
			if getattr(server_cls, 'address_family') == socket.AF_INET:
				class server_cls(server_cls):
					address_family = socket.AF_INET6

		srv = make_server(self.host, self.port, app, server_cls, handler_cls)
		self.srv = srv ### THIS IS THE ONLY CHANGE TO THE ORIGINAL CLASS METHOD!
		srv.serve_forever()

	def shutdown(self): ### ADD SHUTDOWN METHOD.
		self.srv.shutdown()

def start_server():
	def begin(server):
		run(server=server)

	server = TestWSGIServer(host=host, port=port)
	Thread(target=begin, args=(server, )).start()

	return server

if __name__ == '__main__':
	timestamp = reset_db()

	server = start_server()
	sleep(timeout) # give server time to start

	expected = "Berlin, 52.520007,13.404954\nBrasilia, -14.235004,-51.92528\nLondon, 51.507351,-0.127758\nMecca, 21.389082,39.857912\nMilano, 45.465422,9.185924\nNew York, 40.712784,-74.005941\nSofia, 42.697708,23.321868"
	test_service(root_url + "/at", expected)
	expected = "42.697708,23.321868"
	test_service(root_url + "/at?name=sofia", expected)
	expected = "42.7,23.0"
	test_service(root_url + "/at?name=sofia&latitude=42.7&longitude=23", expected)
	test_service(root_url + "/at?name=sofia", expected)
	test_service(root_url + "/where")
	test_service(root_url + "/where/sofia", expected)
	test_service(root_url + "/where/sofia/42.697708/23.321868")
	expected = "Berlin, 52.520007,13.404954\nBrasilia, -14.235004,-51.92528\nLondon, 51.507351,-0.127758\nMecca, 21.389082,39.857912\nMilano, 45.465422,9.185924\nNew York, 40.712784,-74.005941\nSofia, 42.697708,23.321868"
	test_service(root_url + "/at", expected)
	print("Service tests passed!")

	server.shutdown()
	sleep(timeout) # give server time to stop
	restore_db(timestamp)
