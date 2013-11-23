"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from likay.accounts.models import Subscriber
from likay.core.models import Location


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class InboundSMSTest(TestCase):
    def user_subscribe_city(self):
        """
        A user will subscribe to a single city
        """

        pass
