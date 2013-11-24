from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
	url(r'^send_sms$', 'send_sms', name="send_sms"),
)