# Python Imports

# Django Imports
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from accounts.forms import MessageForm
from sms.utils import send_sms
from accounts.models import Subscriber, Moderator


@login_required
def send_sms(request, template_name="accounts/send_sms.html"):
	"""
	View that will let the moderator send sms
	"""
	ctx = {}

	moderator = Moderator.objects.get(user=request.user)
	ctx['moderator'] = moderator

	if request.method == "POST":
		data = request.POST

		form = MessageForm(data)
		if form.is_valid():
			message = form.save(commit=False)
			message.location = moderator.location
			message.moderator = moderator
			message.save()

			subscribers = Subscriber.objects.filter(location__in=[moderator.location])

			for subscriber in subscribers:
				send_sms(subscriber.phone, message.content)

		return HttpResponseRedirect(reverse('send_sms'))			

	else:
		form = MessageForm()

	ctx['form'] = form
	return render_to_response(template_name, ctx,
		context_instance=RequestContext(request))