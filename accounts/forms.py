from django import forms

from sms.models import Message


class MessageForm(forms.ModelForm):
	"""
	Message Form
	"""
	class Meta:
		model = Message
		exclude = ['date_received', 'moderator', 'subscriber', 'location',]