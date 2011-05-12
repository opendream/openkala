from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^test/', 'quarter.views.test'),
    url(r'^post', 'quarter.views.postMSG'),
    url(r'^oldproject', 'quarter.views.project_page'),

    url(r'^api/', include('api.urls')),

    url(r'^$', 'quarter.views.project_list', name='home'),
    url(r'^projects$', 'quarter.views.project_list', name='quarter_project_list'),
    url(r'^projects/(?P<project_id>[^/]+)$', 'quarter.views.project_overview', name='quarter_project_overview'),
    url(r'^projects/(?P<project_id>[^/]+)/plans$', 'quarter.views.plan_overview', kwargs={'week': 1}, name='quarter_plan_overview'),
    url(r'^projects/(?P<project_id>[^/]+)/plans/(?P<week>[^/]+)$', 'quarter.views.plan_overview', name='quarter_plan_week'),

    url(r'^projectsExt$', 'quarter.views.project_page'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^utility/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv', 'utility.views.admin_list_export'),
)


urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls'))
    ) + urlpatterns

