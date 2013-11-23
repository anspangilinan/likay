from django.db import models

_optional_kwargs = {
    'null': True,
    'blank': True
}


class Location(models.Model):
    name = models.CharField(max_length = 255, **_optional_kwargs)
    code = models.CharField(max_length = 25, **_optional_kwargs)

    def __unicode__(self):
        return "%s" % self.name

class Status(models.Model):
    """
    Status of the weather; Parsed from the Weather API;
    """
    name = models.CharField(max_length = 255, **_optional_kwargs)
