from django.conf.urls import patterns, include, url

urlpatterns = patterns('sms.views',
    url(r'^inbound/$', 'inbound_sms', name="inbound_sms"),
    url(r'^message/$', 'post_message', name="post_message"),
)
