import requests
import twitter

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