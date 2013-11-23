from django.contrib import admin

from accounts.models import Subscriber
from core.models import Location, Status
from sms.models import Message, MessageTemplate


class SubscriberAdmin(admin.ModelAdmin):
	model = Subscriber
	filter_horizontal = ['location']

admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Location)
admin.site.register(Status)
admin.site.register(Message)
admin.site.register(MessageTemplate)
