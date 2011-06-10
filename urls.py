from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'quarter.views.home', name='home'),
    url(r'^api/', include('api.urls')),
    #url(r'^accounts/login$', 'quarter.views.accounts_login', name='accounts_login'),

    # quarter
    url(r'^projects$', 'quarter.views.project_list', name='quarter_project_list'),
    url(r'^projects/(?P<project_id>[^/]+)$', 'quarter.views.project_overview', name='quarter_project_overview'),
    url(r'^standard-headers$', 'quarter.views.standard_header_list', name='quarter_standard_header_list'),

    # other
    url(r'^utility/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)\.csv', 'utility.views.admin_list_export'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
)


urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls'))
    ) + urlpatterns

