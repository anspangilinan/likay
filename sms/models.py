from django.db import models
from accounts.models import Subscriber
from core.models import Location, Status


_optional_kwargs = {
    'null': True,
    'blank': True
}

class Message(models.Model):
    """
    Messages received via SMS API
    @property content    - Message by subscribers
    @property location   - Subscribers location so as we message could be filtered by location (Optional field)
    @property subscriber - Subcriber sending the message
    """
    content    = models.TextField(**_optional_kwargs)
    location   = models.OneToOneField(Location, **_optional_kwargs)
    subscriber = models.OneToOneField(Subscriber, **_optional_kwargs)

    def __unicode__(self):
        return "Message ID: %s - %s" % (self.id, self.content)


class MessageTemplate(models.Model):
    """
    Message Templates that would be sent by the app or by admin manually
    @property content - Template of the message to be sent
    @property status  - Status that the message will be sent
    """
    content = models.TextField(**_optional_kwargs)
    status  = models.OneToOneField(Status, **_optional_kwargs)

    def __unicode__(self):
        return "Message ID: %s - %s" % (self.id, self.content)
