from django.conf.urls import patterns, include, url



urlpatterns = patterns('sms.views',
	url(r'^fetching$', 'sms', name="fetch_sms"),
)
