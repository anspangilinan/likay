# Python Imports

# Django Imports
from django.http import HttpResponseNotModified
from django.shortcuts import redirect

# Models
from accounts.models import Subscriber
from core.models import Location
from sms.models import Message

# Utils
from sms.utils import post_to_twitter, post_to_facebook


# KEYWORDS *note: value should be unicode
KEYWORD = {
    'subscribe'  : u'SUB',
    'unsubscribe': u'UNSUB',
    'message'    : u'MSG',
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
            subscribe(content)
        elif KEYWORD['unsubscribe'] == content['text'][0]:
            unsubscribe(content)
        elif KEYWORD['message'] == content['text'][0]:
            post_message(content)
        else:
            pass
            # TO-DO: Send sms to user that their sms format is invalid
        return HttpResponseNotModified()
    else:
        return redirect('index')


def subscribe(data):
    """
    This function will check and save the user's data
    """
    # Get location
    location = Location.objects.filter(code=data['text'][1])

    if location.exists():
        # Check if the number already exist in the database
        subscriber, created = Subscriber.objects.get_or_create(phone=data['num'])
        if created:
            # Save name (optional)
            name = ' '.join(data['text'][2:])
            if name:
                subscriber.name = name
        subscriber.location.add(location[0])
        subscriber.save()
    else:
        # Send SMS to the user that the CITY is not valid
        pass


def unsubscribe(data):
    """
    This function will check and unscubscribe the user's data
    """
    # Slice the text format: TYPE<space>CITY<space>NAME
    location = Location.objects.filter(code=data['text'][1])
    subscriber = Subscriber.objects.filter(phone=data['num'])

    if subscriber.exists() and data['text'][1] == 'ALL':
        subscriber = subscriber[0]
        subscriber.location.clear()
        # TO-DO: confirmation reply that user is not subscribed
        # to any cities anymore
    if location.exists() and subscriber.exists():
        subscriber = subscriber[0]
        if location[0] in subscriber.location.all():
            subscriber.location.remove(location[0])
            subscriber.save()
        else:
            # user is not subscribed to the city
            pass
    else:
        # location and user does not exist: do something
        pass


def post_message(data):
    """
    This function will save the message and post on:
    - ShoutOut Board
    - Facebook
    - Twitter
    """
    # Slice the text format: TYPE<space>CITY<space>NAME
    try:
        message = data['text'][1]
        subscriber = Subscriber.objects.get(phone=str(data['from'][0]))
    except IndexError, e:
        # Error: Send error message
        pass
    except Subscriber.DoesNotExist, e:
        # Error: Send error message
        pass
    else:
        # Save Message
        message = Message.objects.create(content=message,
                                         subscriber=subscriber)
        message.save()
        # Add Facebook and twitter post here
        post_to_twitter(data['text'][0])
        post_to_facebook(data['text'][0])

