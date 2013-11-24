from django.db import models


_optional_kwargs = {
    'null': True,
    'blank': True
}

class Location(models.Model):
    name      = models.CharField(max_length = 255, **_optional_kwargs)
    code      = models.CharField(max_length = 25, **_optional_kwargs)
    latitude  = models.CharField(max_length = 255, **_optional_kwargs)
    longitude = models.CharField(max_length = 255, **_optional_kwargs)

    def __unicode__(self):
        return "%s" % self.name


class Status(models.Model):
    """
    Status of the weather; Parsed from the Weather API;
    """
    name = models.CharField(max_length = 255, **_optional_kwargs)


class InboundSMS(models.Model):
    svc_id = models.CharField(max_length=255, **_optional_kwargs)
    rrn = models.CharField(max_length=255, **_optional_kwargs)
    sender = models.CharField(max_length=255, **_optional_kwargs)
    text = models.TextField(**_optional_kwargs)
    smsc = models.CharField(max_length=255, **_optional_kwargs)
    utime = models.CharField(max_length=255, **_optional_kwargs)
    to = models.CharField(max_length=255, **_optional_kwargs)

    def __unicode__(self):
        return "%s - %s" % (self.sender, self.text)
