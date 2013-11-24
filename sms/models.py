import datetime

from django.db import models
from accounts.models import Subscriber, Moderator
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
    content       = models.TextField(**_optional_kwargs)
    location      = models.ForeignKey(Location, **_optional_kwargs)
    subscriber    = models.ForeignKey(Subscriber, **_optional_kwargs)
    moderator     = models.ForeignKey(Moderator, **_optional_kwargs)
    date_received = models.DateTimeField(**_optional_kwargs)

    def __unicode__(self):
        return "Message ID: %s - %s" % (self.id, self.content)

    def save(self,*args,**kwargs):
        if not self.id:
            self.date_received = datetime.datetime.now()
        super(Message, self).save(*args, **kwargs)


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
