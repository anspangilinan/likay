from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'likay.views.index', name='index'),
    # url(r'^likay/', include('likay.foo.urls')),
    url(r'^sms/', include('sms.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
)
