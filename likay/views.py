from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Location
from sms.models import Message


def index(request, template="index.html"):
    context = {}
    cities = Location.objects.all().order_by("name")

    # Feeds
    messages = Message.objects.all().order_by('-date_received')

    context = {
        "cities": cities,
        "messages": messages,
    }
    
    return render_to_response(template, context, RequestContext(request))