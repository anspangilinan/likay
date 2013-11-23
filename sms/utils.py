import requests

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
