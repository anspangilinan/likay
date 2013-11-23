from django.conf.urls import patterns, include, url

urlpatterns = patterns('sms.views',
    url(r'^inbound/$', 'sms', name="fetch_sms"),
)
