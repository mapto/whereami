import numpy as np

# The geolocators in geopy that do not expect api_key
from geopy.geocoders import GeocodeFarm, Yandex, ArcGIS

locators = [GeocodeFarm(), Yandex(), ArcGIS()]

class Coordinates:
	def __init__(self, latitude, longitude):
		self.latitude=latitude
		self.longitude=longitude

def reject_outliers(data, alpha = 90):
	mask = (data.lat < np.percentile(data.lat, alpha)) & (data.long < np.percentile(data.long, alpha))
	return data[mask]

def geocode(address):
	#candidates = np.array([], dtype=[('long',float),('lat', float)])
	candidates = []
	for locator in locators:
		rloc = locator.geocode(address)
		if rloc:
			#print(rloc.raw)
			candidates.append((rloc.latitude, rloc.longitude))
			#coords = np.core.records.fromrecords([x.values() for x in candidates], names=candidates[0].keys())
			#candidates.append(rloc)
			#a = np.array([(1, 2.0), (1, 2.0)], dtype=[('x', int), ('y', float)])
	coords = np.core.records.fromrecords(candidates, names='lat,long')
	if len(coords) > 2:
		coords = reject_outliers(coords)
	#return {"latitude": np.average(coords.lat), "longitude": np.average(coords.long)}
	return Coordinates(np.average(coords.lat), np.average(coords.long))

if __name__ == '__main__':
	result = geocode("VIA DELLA CASETTA MATTEI 205")
	print(result)
