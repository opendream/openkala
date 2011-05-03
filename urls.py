from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^test/', 'quarter.views.test'),
    url(r'^post', 'quarter.views.postMSG'),
    # Examples:
    # url(r'^$', 'openkala.views.home', name='home'),
    # url(r'^openkala/', include('openkala.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^projects$', 'quarter.views.project_list'),
    url(r'^projects/(?P<project_id>[^/]+)$', 'quarter.views.project_overview'),
    url(r'^projects/(?P<project_id>[^/]+)/topics$', 'quarter.views.project_overview'),
    url(r'^projects/(?P<project_id>[^/]+)/topics/(?P<topic_id>[^/]+)$', 'quarter.views.topic_overview'),
    url(r'^projects/(?P<project_id>[^/]+)/topics/(?P<topic_id>[^/]+)/plans/(?P<plan_id>[^/]+)$', 'quarter.views.plan_overview'),
    #url(r'^topics/(?P<topic_id>[^/]+)/plans/(?P<plan_id>[^/]+)$', 'quarter.views.plan_list'),

    url(r'^projectsExt$', 'quarter.views.project_page'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls'))
    ) + urlpatterns

