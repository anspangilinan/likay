#!/usr/bin/env python
import os
import sys
import requests
import json

# Storm Category
# - Signal no. 1 - 30-60kph
# - Signal no. 2 - 60-100kph
# - Signal no. 3 - 100-185kph
# - Signal no. 4 - 185kph up

def fetch_weather_data():
	from accounts.models import Subscriber
	from sms.utils import send_sms
	weather_query = "http://api.wunderground.com/api/e8f40aeb79ff08f8/currenthurricane/view.json"
	response = json.loads(requests.get(weather_query).content)
	hurricanes = response['currenthurricane']
	#for development simulation
	hurricanes = [{
	 'forecast': [{
	 	'lat': 7.0644,
		'lon': 125.6078,
		'WindSpeed': {
			'Kph': 120,
		},
		'WindGust': {
			'Kph': 120,
		}
	 }]
	}]
	
	for hurricane in hurricanes:
		current_forecast = hurricane['forecast'][-1]
		latitude = current_forecast['lat']
		longitude = current_forecast['lon']

		nearby_location = get_nearby_location(latitude, longitude)
		if (nearby_location):
			wind_speed = current_forecast['WindSpeed']['Kph']
			wind_gust = current_forecast['WindGust']['Kph']

			sms_message = """%s has been issued on %s with a wind speed of %f Kph and a wind gust of %f Kph.""" % (compare_storm_signals(wind_speed), nearby_location.name, wind_speed, wind_gust)
			subscribers = Subscriber.objects.filter(location__name__iexact=nearby_location.name)

			for subscriber in subscribers:
				send_sms(subscriber.phone, sms_message)

	return 'success'


def compare_storm_signals(wind_speed):
	if wind_speed > 30 and wind_speed <=60:
		return 'Storm Signal No. 1.'
	elif wind_speed > 60 and wind_speed <=100:
		return 'Storm Signal No. 2'
	elif wind_speed > 100 and wind_speed <=185:
		return 'Storm Signal No. 3'
	elif wind_speed > 185:
		return 'Storm Signal No. 4'


def get_nearby_location(latitude, longitude):
	from core.models import Location
	location_query = "http://ws.geonames.org/findNearbyPlaceNameJSON?lat=%f&lng=%f&username=ferower" % (latitude, longitude)
	print "location query: "
	response = json.loads(requests.get(location_query).content)
	if response.has_key('geonames'):
		print "geonames"
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








