import requests
import twitter
import facebook
import pusher

from django.conf import settings

from core.models import Location


def send_sms(number, message):
    """
    Send SMS to the number
    Parameters:
    - number: must be in international format (e.g: '639177169495')
              NOTE: no '+' sign before the number
    - text:   should be in UTF8 format
    """
    params = {
        'accountId': settings.ACCOUNT_ID,
        'msisdn': number,
        'text': message
    }

    if not settings.YOUPHORIC_TEST_MODE:
        send_sms = requests.get(settings.OUTBOUND_URL,
                                params=params)
    else:
        print "======================"
        print params['message']
        print "======================"


def post_to_twitter(message):
    # Create Twitter API instance
    api = twitter.Api(consumer_key = settings.TWITTER_CONSUMER_KEY, 
                      consumer_secret = settings.TWITTER_CONSUMER_SECRET, 
                      access_token_key = settings.TWITTER_ACCESS_TOKEN, 
                      access_token_secret= settings.TWITTER_ACCESS_TOKEN_SECRET)
    # Tweets are limited to 140
    message = "%s... http://likay.ingenuity.ph" % (message[:109])
    status = api.PostUpdate(message)


def post_to_facebook(message):
    """
    This will automatically post to facebook as likayph
    """
    access_token = settings.POST_ACCESS_TOKEN

    facebook_graph = facebook.GraphAPI(access_token)    
    attach = {
        'name':'Likay Shout Out',
        'link':'likay.ingenuity.ph',
        'caption':'MSG<space>YOUR MESSAGE and send to 68002',
        'description': message,
    }

    response = facebook_graph.put_wall_post('', attachment=attach, profile_id=settings.FACEBOOK_PAGE_ID)


def invalid_city_message(city):
    """
    Returns a string of list of suggested cities
    depending on string `city`
    """
    # Send SMS to the user that the CITY is not valid
    message = 'Invalid text format.<CITY> is not valid.'
    # Get suggested cities with first 3 letters of the CITY
    if len(city) == 3:
        suggested_locations = Location.objects.filter(code__istartswith=city[:2])
        if suggested_locations:
            first = True
            for suggested_location in suggested_locations:
                if first:
                    first = False
                    message += ' Suggested City Codes: %s ' % suggested_location.code
                else:
                    message += '- %s' % suggested_location.code
    else:
        suggested_locations = Location.objects.filter(name__istartswith=city[:3])
        if suggested_locations:
            first = True
            for suggested_location in suggested_locations:
                if first:
                    first = False
                    message += ' Suggested City Name: %s ' % suggested_location.name
                else:
                    message += '- %s' % suggested_location.name
    return message


def realtime_post(message):
    p = pusher.Pusher(
      app_id='60123',
      key='4a1b121857529e74584b',
      secret='664908558ecf9f1d5027'
    )
    p['message_channel'].trigger('new_post', {'message': message})
