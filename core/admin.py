from django.contrib import admin

from accounts.models import Subscriber
from core.models import Location, Status
from sms.models import Message, MessageTemplate


admin.site.register(Subscriber)
admin.site.register(Location)
admin.site.register(Status)
admin.site.register(Message)
admin.site.register(MessageTemplate)
