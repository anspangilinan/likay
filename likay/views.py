from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Location


def index(request, template="index.html"):
    context = {}
    cities = Location.objects.all().order_by("name")

    context = {
        "cities": cities
    }
    
    return render_to_response(template, context, RequestContext(request))