"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import urllib

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import Client

from accounts.models import Subscriber
from core.models import Location


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class InboundSMSTest(TestCase):
    """
    Sample GET request from youphoric:
    - <QueryDict: {u'svc_id': [u'0'],
                   u'rrn': [u'410063049520'],
                   u'from': [u'639998419831'],
                   u'text': [u'Patty hello'],
                   u'smsc': [u'strikerS6800in1ngin'],
                   u'to': [u'68002'],
                   u'utime': [u'1385197861']}>
    - The only vital data from their request is the 'from' and 'text' values
    """
    def setUp(self):
        self.url = reverse('inbound_sms') + '?'
        self.client = Client()
        self.num = '639177169495'
        self.test_location = Location.objects.create(name='Davao',
                                                     code='DVO')
        self.test_user = Subscriber.objects.create(name='Test Name',
                                                   phone=self.num)
        self.bad_request_code = 400

    def test_invalid_text_format(self):
        """
        User texts to the number using an invalid format
        Examples:
        - BUS DVO
        - Hello
        - WUT
        """
        sample_text = 'WUT THE HELL'
        test_get = {
            'from': self.num,
            'text': sample_text,
        }
        url = self.url + urllib.urlencode(test_get)
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         self.bad_request_code)

    def test_user_subscribe_existing_city_subscription(self):
        """
        User subscribes again for a city already subscribed
        """
        self.test_user.location.add(self.test_location)
        city = 'DVO'
        test_get = {
            'from': self.num,
            'text': 'SUB %s' % city,
        }
        url = self.url + urllib.urlencode(test_get)
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         self.bad_request_code)

    def test_user_subscribe_valid_city_no_name(self):
        """
        A user will subscribe to a single city
        Examples:
        - SUB DVO
        - SUB Davao
        - SUB Manila
        """
        city = 'DVO'
        test_get = {
            'from': self.num,
            'text': 'SUB %s' % city,
        }
        url = self.url + urllib.urlencode(test_get)
        response = self.client.get(url)
        user = Subscriber.objects.filter(phone=self.num,
                                         location__code=city)
        self.assertEqual(user.exists(),True)

    def test_user_subscribe_valid_city_with_name(self):
        """
        A user will subscribe to a single city and also pass his name.
        The name string after the city name will be considered the user's name
        Examples:
        - SUB DVO Joseph Lafuente
        - SUB Manila Siyopapi Basoc
        - SUB BOR Earvin P. Gemenez
        """
        city = 'DVO'
        test_get = {
            'from': self.num,
            'text': 'SUB %s %s' % (city, self.test_user.name),
        }
        url = self.url + urllib.urlencode(test_get)
        response = self.client.get(url)
        user = Subscriber.objects.filter(phone=self.num,
                                         location__code=city,
                                         name=self.test_user.name)
        self.assertEqual(user.exists(), True)

    def test_user_subscribe_invalid_city(self):
        """
        A user will subscribe but the city specified in the text is not
        in the database
        """
        city = 'INVALIDCITY'
        test_get = {
            'from': self.num,
            'text': 'SUB %s' % city,
        }
        url = self.url + urllib.urlencode(test_get)
        response = self.client.get(url)
        user = Subscriber.objects.filter(phone=self.num,
                                         location__code=city)

        self.assertEqual(not user.exists(), True)
        self.assertEqual(response.status_code,
                         self.bad_request_code)

    def test_user_unsubscribe_valid_city(self):
        """
        Existing user unsubscribes to a valid city given the user
        is subscribed to that city
        """
        city = 'DVO'
        test_get = {
            'from': self.num,
            'text': 'UNSUB %s' % city,
        }
        self.test_user.location.add(self.test_location)
        url = self.url + urllib.urlencode(test_get)
        response = self.client.get(url)
        city_still_subscribed = self.test_location in self.test_user.location.all()
        self.assertEqual(city_still_subscribed, False)

    def test_user_unsubscribe_invalid_city(self):
        """
        Existing user unsubscribes to an invalid city.
        An invalid city is (1) not in the database or
                           (2) user is not subscribed to that city
        """
        city = 'INVALIDCITY'
        test_get = {
            'from': self.num,
            'text': 'UNSUB %s' % city,
        }
        url = self.url + urllib.urlencode(test_get)
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         self.bad_request_code)

    def test_user_unsubscribe_all(self):
        """
        Existing user unsubscribes to all cities
        (regardless if user is subscribed to a city or not)
        """
        test_get = {
            'from': self.num,
            'text': 'UNSUB ALL'
        }
        url = self.url + urllib.urlencode(test_get)
        response = self.client.get(url)
        no_subscribed_cities = not self.test_user.location.all()
        self.assertEqual(no_subscribed_cities, True)

    def test_group_sub(self):
        """
        An existing user sends a list of numbers separated by comma
        and a city name. The numbers will be subscribed to weather updates
        of the city specified
        """
        city = 'DVO'
        test_get = {
            'from': self.num,
            'text': 'GRPSUB %s 639177169495,639177169495,639177169495' % city,
        }
        url = self.url + urllib.urlencode(test_get)
        response = self.client.get(url)