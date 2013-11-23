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

			sms_message = """%s Weather Advisory: %s""" % (nearby_location.name, compare_storm_signals(wind_speed))
			subscribers = Subscriber.objects.filter(location__name__iexact=nearby_location.name)

			for subscriber in subscribers:
				send_sms(subscriber.phone, sms_message)

	return 'success'


def compare_storm_signals(wind_speed):
	if wind_speed > 30 and wind_speed <=60:
		return 'StormSignal#1-Listen to the latest severe weather bulletin issued by PAGASA'
	elif wind_speed > 60 and wind_speed <=100:
		return 'StormSignal#2-People traveling by sea and air take caution;Secure properties'
	elif wind_speed > 100 and wind_speed <=185:
		return 'StormSignal#3-Air/Sea travel very risky;Sseek shelter in strong buildings;Evacuate low-lying areas;Stay away from the coasts/riverbanks'
	elif wind_speed > 185:
		return 'StormSignal#4-Situation potentially very destructive to community;Cancel all travels/outdoor activities;Evacuate now'


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








