#!/usr/bin/env python
import os
import sys
import requests
import json

def fetch_weather_data():
	# http://api.wunderground.com/api/e8f40aeb79ff08f8/geolookup/conditions/q/ph/manila.json
	weather_query = "http://api.wunderground.com/api/e8f40aeb79ff08f8/currenthurricane/view.json"
	response = json.loads(requests.get(weather_query).content)
	hurricanes = response['currenthurricane']
	#for development simulation
	# hurricanes = [{
	#  'forecast': [{
	#  	'lat': 7.0644,
	# 	'lon': 125.6078,
	#  }]
	# }]
	
	for hurricane in hurricanes:
		current_forecast = hurricane['forecast'][-1]
		latitude = current_forecast['lat']
		longitude = current_forecast['lon']

		nearby_location = get_nearby_location(latitude, longitude)
		if (nearby_location):
			print "send sms to " + nearby_location.name
			# send_sms(nearby_location)
	return 'success'


def get_nearby_location(latitude, longitude):
	from core.models import Location
	location_query = "http://api.geonames.org/findNearbyPlaceNameJSON?lat=%f&lng=%f&username=ferower" % (latitude, longitude)
	response = json.loads(requests.get(location_query).content)
	place_names = response['geonames']
	if len(place_names) > 0:
		place_name = place_names[0]['toponymName']
		match_location = Location.objects.filter(name__iexact=place_name)
		if match_location.count() > 0:
			return match_location[0]
	return False


if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "likay.settings")
	from django.core.management import setup_environ
	import likay.settings as settings
	setup_environ(settings)
	fetch_weather_data()








