from django.conf.urls.defaults import *

urlpatterns = patterns('dps.views',
    (r'^success/(?P<token>.*)$', 'transaction_success'),
    (r'^failure/(?P<token>.*)$', 'transaction_failure'),
)
