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
    url(r'^projects/(?P<project_id>[^/]+)/plans$', 'quarter.views.plan_overview', kwargs={'plan_week': 1}),
    url(r'^projects/(?P<project_id>[^/]+)/plans/(?P<plan_week>[^/]+)$', 'quarter.views.plan_overview', name='quarter_plan'),
    url(r'^projects/(?P<project_id>[^/]+)/blogs$', 'quarter.views.blog_list', name='quarter_blog_list'),
    url(r'^projects/(?P<project_id>[^/]+)/blogs/(?P<blog_id>[^/]+)$', 'quarter.views.blog_detail', name='quarter_blog_detail'),
    
    # gallery
    url(r'^projects/(?P<project_id>[^/]+)/stockphoto$', 'stockphoto.views.gallery_list', name='stockphoto_gallery_list'),
    url(r'^projects/(?P<project_id>[^/]+)/stockphoto/add$', 'stockphoto.views.gallery_add', name='stockphoto_gallery_add'),
    url(r'^projects/(?P<project_id>[^/]+)/stockphoto/(?P<gallery_id>[^/]+)$', 'stockphoto.views.gallery_detail', name='stockphoto_gallery_detail'),
    url(r'^projects/(?P<project_id>[^/]+)/stockphoto/detail/(?P<photo_id>[^/]+)$', 'stockphoto.views.photo_detail', name='stockphoto_photo_detail'),
    url(r'^projects/(?P<project_id>[^/]+)/stockphoto/detail/(?P<photo_id>[^/]+)/delete$', 'stockphoto.views.photo_delete', name='stockphoto_photo_delete'),
    url(r'^projects/(?P<project_id>[^/]+)/getmode$', 'quarter.views.project_getmode'),
    url(r'^projects/(?P<project_id>[^/]+)/setmode/(?P<mode>[^/]+)$', 'quarter.views.project_setmode'),

    url(r'^projects/(?P<project_id>[^/]+)/import/(\d+)/$', 'stockphoto.views.import_photos', name="stockphoto_import"),
    url(r'^projects/(?P<project_id>[^/]+)/export/(\d+)/$', 'stockphoto.views.export', name="stockphoto_export"),


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

