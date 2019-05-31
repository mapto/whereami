"""Initialization of geolocation services commonly contains private keys.
if no keys present, add yours.
Options can be seen in geopy.geocoders.SERVICE_TO_GEOCODER
"""
import geopy
# The geolocators in geopy that do not expect api_key
selected_locators = {
    "arcgis": geopy.geocoders.arcgis.ArcGIS(),
    "yandex": geopy.geocoders.yandex.Yandex()
}
