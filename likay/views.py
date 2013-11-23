from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Location
from sms.models import Message
from sms.views import KEYWORD


def index(request, template="index.html"):
    context = {}
    cities = Location.objects.all().order_by("name")

    today = datetime.today()
    start_date = datetime(today.year, today.month, today.day)
    end_date = datetime(today.year, today.month, today.day+1)
    messages = Message.objects.filter(content__startswith=KEYWORD["message"],
                                      date_received__gte=start_date,
                                      date_received__lte=end_date)


    # Feeds
    messages = Message.objects.all().order_by('-date_received')

    context = {
        "cities": cities,
        "messages": messages
    }
    
    return render_to_response(template, context, RequestContext(request))