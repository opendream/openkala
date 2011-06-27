from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.conf import settings

from models import Gallery, Photo, ADMIN_URL, STOCKPHOTO_URL
from views import *

info_dict = { 'extra_context': { 'admin_url': ADMIN_URL,
                                 'stockphoto_url': STOCKPHOTO_URL} }

'''
urlpatterns = patterns('',
	url(r'^$', object_list,
            dict(info_dict, queryset=Gallery.objects.all(),
                 paginate_by=24, allow_empty= True),
            name='stockphoto_gallery_list'),
	url(r'^(?P<object_id>\d+)/$', object_detail,
            dict(info_dict, queryset=Gallery.objects.all()),
            name='stockphoto_gallery_detail'),
	url(r'^detail/(?P<object_id>\d+)/$', object_detail,
            dict(info_dict, queryset=Photo.objects.all()),
            name='stockphoto_photo_detail'),
)
'''

urlpatterns = patterns('',
    url(r'^import/(\d+)/$', import_photos, name="stockphoto_import"),
    url(r'^export/(\d+)/$', export, name="stockphoto_export"),
)
