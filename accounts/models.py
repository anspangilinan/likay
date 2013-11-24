from django.db import models
from core.models import Location
from django.contrib.auth.models import User


_optional_kwargs = {
    'null': True,
    'blank': True
}


class Subscriber(models.Model):
    """
    Users that subscribed via SMS
    """
    phone    = models.CharField(max_length = 50, **_optional_kwargs)
    name     = models.CharField(max_length = 200, **_optional_kwargs)
    location = models.ManyToManyField(Location, **_optional_kwargs)

    def __unicode__(self):
        return "%s" % self.name


class Moderator(models.Model):
    """
    Groups that can send custom sms to specific location
    """
    user     = models.ForeignKey(User)
    location = models.ForeignKey(Location)
