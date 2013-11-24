# Python Imports
import json
import requests
from twitter import TwitterError

# Django Imports
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect

# Models
from accounts.models import Subscriber
from core.models import Location
from sms.models import Message

# Utils
from sms.utils import send_sms, post_to_twitter, post_to_facebook, invalid_city_message, realtime_post

# KEYWORDS *note: value should be unicode
KEYWORD = {
    'subscribe'  : u'SUB',
    'unsubscribe': u'UNSUB',
    'message'    : u'MSG',
    'info'       : u'INFO',
}


def inbound_sms(request):
    """
    This view will catch the user's sms through a GET request from youphoric server.
    """
    if request.method == "GET" and 'text' in request.GET and 'from' in request.GET:
        # TO-DO PAT: check GET if 'smsc' is 'strikerS6800in1ngin' 
        # (and add that to source smsc in settings)?
        content = {
            'text': request.GET['text'].split(),
            'num': request.GET['from']
        }
        if KEYWORD['subscribe'] == content['text'][0]:
            response = subscribe(content)
        elif KEYWORD['unsubscribe'] == content['text'][0]:
            response = unsubscribe(content)
        elif KEYWORD['message'] == content['text'][0]:
            message = request.GET.get('text').replace(KEYWORD['message'] + ' ', '')
            content['text'] = message
            response = post_message(content)
        elif KEYWORD['info'] == content['text'][0]:
            response = info(content)
        else:
            message = 'Invalid Text Format: Formats are the following - SUB <city> <name(optional)>; UNSUB <city>; UNSUB ALL; INFO; MSG <message>;'
            send_sms(content['num'], message)
            return HttpResponse(content=message,
                                status=400)
        return response
    else:
        return redirect('index')


def location_list(city_string):
    location = Location.objects.filter(Q(code__iexact=city_string) | Q(name__iexact=city_string))
    return location


def subscribe(data):
    """
    This function will check and save the user's data
    """
    # Get location
    city = data['text'][1]
    location = location_list(city)

    if location.exists():
        # Check if the number already exist in the database
        subscriber, created = Subscriber.objects.get_or_create(phone=data['num'])
        if created:
            # Save name (optional)
            name = ' '.join(data['text'][2:])
            if name:
                subscriber.name = name
        if location[0] in subscriber.location.all():
            error_message = 'Subscription Error - Subscription to %s already exists' % location[0]
            send_sms(data['num'], error_message)
            return HttpResponse(content=error_message,
                                status=400)
        else:
            subscriber.location.add(location[0])
            subscriber.save()
            success_msg = 'You will now receive important weather updates for the city of %s' % location[0]
            send_sms(data['num'], success_msg)
        return HttpResponse('SUBSCRIBE OK - User subscribed to %s' % location[0])
    else:
        # Send SMS to the user that the CITY is not valid
        message = invalid_city_message(city)
        send_sms(data['num'], message)
        return HttpResponse(content='SUBSCRIBE ERROR - Invalid city: %s' % data['text'][1],
                            status=400)


def unsubscribe(data):
    """
    This function will check and unscubscribe the user's data
    """
    # Slice the text format: TYPE<space>CITY<space>NAME
    city = data['text'][1]
    location = location_list(city)
    subscriber = Subscriber.objects.filter(phone=data['num'])

    if subscriber.exists() and data['text'][1] == 'ALL':
        subscriber = subscriber[0]
        subscriber.location.clear()
        success_msg = "You will stop receiving weather updates from cities anymore."
        send_sms(data['num'], success_msg)
        return HttpResponse(success_msg)
    if location.exists() and subscriber.exists():
        subscriber = subscriber[0]
        if location[0] in subscriber.location.all():
            subscriber.location.remove(location[0])
            subscriber.save()
            success_msg = 'You will stop receiving weather updates for the city of %s.' % location[0]
            send_sms(data['num'], success_msg)
            return HttpResponse(success_msg)
        else:
            # user is not subscribed to the city
            error_msg = 'Unsubscription Error: You are not subscribed to %s.' % location[0]
            send_sms(data['num'], error_msg)
            return HttpResponse(content=error_msg,
                                status=400)
    else:
        message = 'You do not have subscriptions to any city yet.' % location[0]
        send_sms(data['num'], message)
        return HttpResponse(content='UNSUBSCRIBE ERROR - Subscriber and location does not exist',
                            status=400)


def post_message(data):
    """
    This function will save the message and post on:
    - ShoutOut Board
    - Facebook
    - Twitter
    """
    # Slice the text format: TYPE<space>CITY<space>NAME
    try:
        message = data['text']
        subscriber = Subscriber.objects.get(phone=str(data['num']))
    except IndexError, e:
        # Error: Send error message
        return HttpResponse(content='MSG ERROR',
                            status=400)
    except Subscriber.DoesNotExist, e:
        # Error: Send error message
        message = "You haven't subscribed yet. To subscribe text SUB <CITY> and send to %s." % settings.ACCESS_CODE
        send_sms(data['num'], message)
        return HttpResponse(content='MSG ERROR - Subscriber does not exist',
                            status=400)
    else:
        # Save Message
        message = Message.objects.create(content=message,
                                         subscriber=subscriber)
        message.save()
        try:
            post_to_twitter(data['text'])
        except TwitterError, t:
            # Duplicate tweets error
            pass
        post_to_facebook(data['text'])
        realtime_post(data['text'])
        return HttpResponse("MSG OK - MESSAGE SENT!")


def info(data):
    """
    Sends SMS message to subscriber regarding 
    weather info on their subscribed city/cities
    """
    try:
        num = str(data['num'])
        subscriber = Subscriber.objects.get(phone=num)
        # http://api.wunderground.com/api/e8f40aeb79ff08f8/geolookup/conditions/q/ph/manila.json
        locations = subscriber.location.all()
        # Send messages for all locations of subscriber
        for location in locations:
            weather_query = "http://api.wunderground.com/api/e8f40aeb79ff08f8/geolookup/conditions/q/ph/%s.json" % location.name.lower()
            response = json.loads(requests.get(weather_query).content)
            observation = response['current_observation']
            message = "WeatherInfo - %s; %s; %s" % (observation['display_location']['city'], 
                                                    observation['weather'],
                                                    observation['temperature_string'])
            send_sms(num, message)
        return HttpResponse('INFO OK')
    except Subscriber.DoesNotExist, e:
        # Error: send error message
        message = "You haven't subscribed yet. To subscribe text SUB <CITY> and send to %s." % settings.ACCESS_CODE
        send_sms(data['num'], message)
        return HttpResponse(content='INFO ERROR - You need to subscribe',
                            status=400)
