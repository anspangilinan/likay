import json
import requests
from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext

from accounts.models import Subscriber
from core.models import Location
from sms.models import Message
from sms.views import KEYWORD


def index(request, template="index.html"):
    context = {}
    cities = []

    today = datetime.today()
    start_date = datetime(today.year, today.month, today.day)
    end_date = datetime(today.year, today.month, today.day+1)

    messages = Message.objects.filter(content__startswith=KEYWORD["message"],
                                      date_received__gte=start_date,
                                      date_received__lte=end_date)
    
    for location in Location.objects.all():
        # weather_query = "http://api.wunderground.com/api/e8f40aeb79ff08f8/geolookup/conditions/q/ph/%s.json" % location.name.lower()
        # response = json.loads(requests.get(weather_query).content)
        # observation = response['current_observation']
        # weather_status = "WeatherInfo - %s; %s" % (observation['weather'],
        #                                         observation['temperature_string'])
        weather_status = "BE WARY, shaparoosh"
        cities.append({
            "city": location,
            "weather_status": weather_status,
            "subscribers": Subscriber.objects.filter(location=location).count()
        })

    # Feeds
    messages = Message.objects.all().order_by('-date_received')

    context = {
        "messages": messages,
        "cities": cities
    }
    
    return render_to_response(template, context, RequestContext(request))