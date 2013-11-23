import requests
import twitter
import facebook
import pusher

from django.conf import settings


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

    import pdb
    pdb.set_trace()

    if not settings.YOUPHORIC_TEST_MODE:
        send_sms = requests.get(settings.OUTBOUND_URL,
                                params=params)


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
        'caption':'MSG<space>YOUR MESSAGE',
        'description': message,
    }

    response = facebook_graph.put_wall_post('', attachment=attach, profile_id=settings.FACEBOOK_PAGE_ID)


def realtime_post(message):
    p = pusher.Pusher(
      app_id='60123',
      key='4a1b121857529e74584b',
      secret='664908558ecf9f1d5027'
    )
    p['message_channel'].trigger('new_post', {'message': message})
