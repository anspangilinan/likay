from django.db import models
from core.models import Location

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
