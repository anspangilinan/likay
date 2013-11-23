# Python Imports

# Django Imports
from django.http import HttpResponse

# Models
from accounts.models import Subscriber
from core.models import Location


# KEYWORDS *note: value should be unicode
KEYWORD = {
    'subscribe': u'SUB',
    'unsubscribe': u'UNSUB',
}

def sms(request):
    """
    This view will catch the user's sms through a GET request from youphoric server.
    """
    if request.method == "GET":
        data = {u'svc_id': [u'0'], u'rrn': [u'410063049575'], u'from': [u'639998419831'], u'text': [u'SUB DVO earvin'], u'smsc': [u'strikerS6800in1ngin'], u'to': [u'68002'], u'utime': [u'1385197906']}

        # Slice the text format: TYPE<space>CITY<space>NAME
        content = data['text'][0].split(' ')

        # Check what type of sms [SUB, UNSUB]
        if KEYWORD['subscribe'] == content[0]:
            print "subscribe"
            subscribe(data)

        elif KEYWORD['unsubscribe'] == content[0]:
            print "unsubscribe"
            unsubscribe(data)
        else:
            pass
            # Will send sms to user that their sms format is invalid

    return HttpResponse("awesomeness!")


def subscribe(data):
    """
    This function will check and save the user's data
    """
    # Slice the text format: TYPE<space>CITY<space>NAME
    content = data['text'][0].split(' ')

    # Get location
    location = Location.objects.get(code=str(content[1]))

    # Check if the number already exist in the database
    subscriber, created = Subscriber.objects.get_or_create(phone=str(data['from'][0]))
    if created:
        subscriber.name = content[2]

    subscriber.location.add(location)
    subscriber.save()


def unsubscribe(data):
    """
    This function will check and unscubscribe the user's data
    """
    # Slice the text format: TYPE<space>CITY<space>NAME
    content = data['text'][0].split(' ')

    # Get location
    location = Location.objects.get(code=str(content[1]))

    subscriber = Subscriber.objects.get(phone=str(data['from'][0]))
    subscriber.location.remove(location)
    subscriber.save()